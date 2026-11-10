"""Interfaz Streamlit para generar reportes de Pizarra Snap."""

import logging
from pathlib import Path
from shutil import copyfileobj
from tempfile import TemporaryDirectory

import streamlit as st

from pipeline import procesar_video


logger = logging.getLogger(__name__)


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


def main():
    st.set_page_config(page_title="Pizarra Snap", page_icon="📸")
    st.title("Pizarra Snap")
    st.write("Convertí un video de tu pizarra en un reporte PDF.")

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

    if st.button("Generar PDF", type="primary", disabled=not video_valido):
        limpiar_resultado()
        try:
            with st.spinner("Procesando el video y generando el PDF…", show_time=True):
                st.session_state.resultado_pdf = generar_pdf(video)
        except ValueError:
            logger.exception("No se pudo procesar el video adjunto")
            st.error(
                "No se pudo procesar el video. Revisá que el MP4 se pueda reproducir "
                "y que las tres zonas de la pizarra estén dentro del encuadre."
            )
        except Exception:
            logger.exception("No se pudo generar el reporte")
            st.error("No se pudo generar el PDF. Volvé a intentarlo.")

    resultado = st.session_state.get("resultado_pdf")
    if resultado is None:
        return

    pdf, resumen = resultado
    st.success("El PDF está listo para descargar.")
    if resumen["total_capturas"] == 0:
        st.warning("No se detectaron capturas en el video.")
    st.caption(
        f"Capturas **{resumen['total_capturas']}** · "
        f"Temas **{resumen['total_temas']}** · "
        f"Páginas **{resumen['paginas_pdf']}**"
    )
    st.download_button(
        "Descargar PDF",
        data=pdf,
        file_name="reporte_pizarra_snap.pdf",
        mime="application/pdf",
        on_click="ignore",
    )


if __name__ == "__main__":
    main()
