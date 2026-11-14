# Contratos del informe

## De la captura a RF13

En [pipeline.py](../../../../pipeline.py), `procesar_capturas()` recibe registros con `tipo_evento`, `momento_del_evento` y `frames_candidatos`. RF12 guarda el PNG original y RF15 puede guardar una versión gris con CLAHE. El resultado incluye `numero_captura`, tipo, momento, métricas y las rutas `captura_path` y `captura_procesada_path`.

`seleccionar_imagen_reporte()` acepta rutas `str` o `Path`. Prefiere una ruta procesada que sea un archivo, después la original. Devuelve la ruta absoluta con `procesada` u `original`, o `(None, "sin_imagen")`. La selección comprueba existencia. Si Pillow falla al abrir la ruta elegida, `_imagen_para_pdf()` muestra un marcador de imagen no disponible.

`adaptar_para_reporte()` exige número entero de captura, evento conocido y un momento convertible a `float`. Mantiene el orden y devuelve registros con `numero_captura`, `tipo_evento`, `categoria`, `momento_del_evento`, `imagen_path` y `fuente_imagen`, sin arrays.

| Evento | Categoría |
|---|---|
| `CAPTURA_NORMAL` | `NORMAL` |
| `CONCEPTO_IMPORTANTE` | `IMPORTANTE` |
| `FIN_DE_TEMA` | `FIN_DE_TEMA` |

## De RF14 al PDF

En [pipeline.py](../../../../pipeline.py), `agrupar_por_temas()` devuelve temas con `numero_tema` desde 1, `capturas` ordenadas y `cerrado`. Incluye la captura `FIN_DE_TEMA` como última del tema que cierra. Las capturas siguientes forman otro tema. Una entrada vacía produce una lista vacía y el último tema sin cierre queda abierto. Rechaza números de captura duplicados y categorías incompatibles.

`generar_pdf_clase(temas, salida_pdf, datos_clase=None)` valida los temas, exige un destino `.pdf`, combina los datos de portada y devuelve el `Path` absoluto de un archivo existente y no vacío. `procesar_video()` abre ese archivo con `PdfReader` para contar páginas y retorna `(ruta_pdf, resumen)`. La base revisada carece de `scripts/validar_pdf.py`.

## Del PDF a la sesión y al correo

En [app.py](../../../../app.py), `generar_pdf()` lee los bytes antes de cerrar el temporal. `main()` conserva `(pdf, resumen)` en `st.session_state.resultado_pdf` y pasa los mismos bytes a descarga y a `mostrar_envio_por_email()`. En [email_sender.py](../../../../email_sender.py), `armar_mensaje()` adjunta esos bytes como `application/pdf` y `enviar_pdf()` usa el nombre predeterminado `reporte_pizarra_snap.pdf`.

La prueba histórica con el MP4 oficial registró tres capturas, un tema cerrado y tres páginas. Para el detalle y su alcance, consultá el [plan de trabajo](../../../../PLAN_TRABAJO_PIZARRA_SNAP.md#16-estado-técnico-consolidado).
