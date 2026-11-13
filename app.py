"""Interfaz Streamlit para generar reportes de Pizarra Snap.

Esta versión solo cambia la presentación. El procesamiento sigue en
`pipeline.procesar_video`, sin modificaciones.
"""

import logging
from pathlib import Path
from shutil import copyfileobj
from tempfile import TemporaryDirectory

import streamlit as st

from pipeline import procesar_video


logger = logging.getLogger(__name__)

COLOR_PRINCIPAL = "#1F7A74"
COLOR_ACENTO = "#F5A623"


def limpiar_resultado():
    st.session_state.pop("resultado_pdf", None)


def generar_pdf(video):
    with TemporaryDirectory(prefix="pizarra_snap_app_") as directorio:
        trabajo = Path(directorio)
        ruta_video = trabajo / "video.mp4"
        video.seek(0)
        with ruta_video.open("wb") as archivo:
            copyfileobj(video, archivo, length=1024 * 1024)
        ruta_pdf, resumen = procesar_video(ruta_video, trabajo)
        return ruta_pdf.read_bytes(), resumen


def mostrar_encabezado():
    st.markdown(
        f"""
        <h1 style="margin-bottom:0">Pizarra <span style="color:{COLOR_ACENTO}">Snap</span></h1>
        <p style="color:#5B6770; font-style:italic; margin-top:0">
            La pizarra que recuerda tu clase.
        </p>
        """,
        unsafe_allow_html=True,
    )
    st.write("Convertí el video de tu pizarra en un reporte PDF organizado por temas.")


def mostrar_instrucciones():
    with st.expander("¿Cómo funciona?", expanded=False):
        st.markdown(
            """
            **1. Grabá la clase** con la cámara fija apuntando a la pizarra. Las tres
            zonas de comando tienen que estar visibles y libres al inicio del video.

            **2. Tapá brevemente una zona** para dar una orden y soltala:

            - 📸 **Captura normal:** guarda una imagen del contenido.
            - ⭐ **Concepto importante:** destaca la captura en el reporte.
            - 📌 **Fin de tema:** guarda la captura y cierra el tema.

            **3. Cargá el video acá**, generá el PDF y descargalo.
            """
        )


def mostrar_resultado(pdf, resumen):
    st.success("El PDF está listo para descargar.")
    if resumen["total_capturas"] == 0:
        st.warning(
            "No se detectaron capturas en el video. Revisá que las tres zonas "
            "estén visibles y que los comandos se hagan tapando la zona unos segundos."
        )

    col_capturas, col_temas, col_paginas = st.columns(3)
    col_capturas.metric("Capturas", resumen["total_capturas"])
    col_temas.metric("Temas", resumen["total_temas"])
    col_paginas.metric("Páginas", resumen["paginas_pdf"])

    st.download_button(
        "Descargar PDF",
        data=pdf,
        file_name="reporte_pizarra_snap.pdf",
        mime="application/pdf",
        type="primary",
        width="stretch",
        on_click="ignore",
    )


def main():
    st.set_page_config(page_title="Pizarra Snap", page_icon="📸", layout="centered")
    mostrar_encabezado()
    mostrar_instrucciones()

    st.divider()
    st.subheader("1. Cargá el video")
    video = st.file_uploader(
        "Adjuntá un video MP4",
        type=["mp4"],
        key="video",
        on_change=limpiar_resultado,
        help="Las tres zonas de la pizarra deben estar visibles al inicio del video.",
    )
    video_valido = video is not None and video.size > 0
    if video is not None and not video_valido:
        st.error("El archivo está vacío. Adjuntá otro video MP4.")
    elif video_valido:
        st.caption(f"Video cargado: **{video.name}** · {video.size / 1_000_000:.1f} MB")

    st.subheader("2. Generá el reporte")
    if st.button(
        "Generar PDF", type="primary", disabled=not video_valido, width="stretch"
    ):
        limpiar_resultado()
        with st.status("Procesando el video…", expanded=True) as estado:
            st.write(
                "Estamos detectando los comandos, eligiendo las mejores capturas "
                "y armando el PDF. Puede tardar unos minutos: no cierres la pestaña."
            )
            try:
                st.session_state.resultado_pdf = generar_pdf(video)
                estado.update(label="Procesamiento terminado", state="complete", expanded=False)
            except ValueError:
                logger.exception("No se pudo procesar el video adjunto")
                estado.update(label="No se pudo procesar el video", state="error")
                st.error(
                    "No se pudo procesar el video. Revisá que el MP4 se pueda reproducir "
                    "y que las tres zonas de la pizarra estén dentro del encuadre."
                )
            except Exception:
                logger.exception("No se pudo generar el reporte")
                estado.update(label="No se pudo generar el PDF", state="error")
                st.error("No se pudo generar el PDF. Volvé a intentarlo.")

    resultado = st.session_state.get("resultado_pdf")
    if resultado is None:
        return

    st.subheader("3. Descargá el reporte")
    pdf, resumen = resultado
    mostrar_resultado(pdf, resumen)


if __name__ == "__main__":
    main()
