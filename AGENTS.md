# Pizarra Snap

Pizarra Snap procesa un MP4 pregrabado de una pizarra y genera un PDF organizado por temas. Usá Python 3.12 y las versiones de [requirements.txt](requirements.txt).

## Arquitectura y fuentes

- [pipeline.py](pipeline.py) implementa RF01–RF16. RF01–RF09 pasan de video y regiones de interés a eventos y candidatos. RF10–RF12 y RF15 seleccionan y guardan la captura con mejora opcional. RF13, RF14 y RF16 clasifican, agrupan y componen el informe.
- [app.py](app.py) gestiona la carga, los temporales y la sesión de Streamlit. `procesar_video(ruta_video, directorio_trabajo)` devuelve la ruta del PDF y un resumen sin imágenes. La app conserva los bytes para descargar o enviar el mismo PDF.
- [email_sender.py](email_sender.py) implementa el transporte de RF17. El envío es opcional y parte del PDF generado. La descarga sigue disponible cuando falta la configuración de correo.
- Consultá el [catálogo RF01–RF17](docs/REQUERIMIENTOS.md), el [plan técnico](PLAN_TRABAJO_PIZARRA_SNAP.md) y el [manual de Colab](notebooks/README.md). Contrastá documentos y código antes de decidir. Registrá las discrepancias que afecten la tarea.

## Desarrollo y revisión

- Delimitá los RF y sus consumidores antes de editar. Conservá contratos, resultados validados, parámetros de visión y diseño del informe salvo que el pedido autorice un cambio. Mantené los aportes históricos y el [notebook de referencia](notebooks/PizarraSnap.ipynb).
- Comprobá rama y estado de Git. Trabajá en una rama de tarea y preservá cambios ajenos. Para publicar, usá la rama autorizada y un PR hacia `main`. Reservá los cambios directos a `main`, el merge y las operaciones destructivas para autorización expresa.
- Revisá únicamente el [ejemplo versionado](.streamlit/secrets.toml.example) para conocer el esquema. Mantené los secretos reales fuera del repositorio, del diff, del chat y de los logs. Usá datos ficticios y simulá el transporte en pruebas.
- Ajustá la validación al cambio. Para documentación comprobá alcance, rutas y `git diff --check`. Para cambios funcionales probá el contrato afectado y sus consumidores. Si cambia el recorrido de video a PDF, usá el MP4 oficial cuando esté disponible y compará los resultados pertinentes con la referencia documentada.
- Informá qué comprobaste, qué resultados observaste y qué quedó pendiente por falta de archivos, permisos o herramientas.

## Skills

- [agregar-requerimiento](.agents/skills/agregar-requerimiento/SKILL.md) guía cambios funcionales y su revisión.
- [informe-pdf](.agents/skills/informe-pdf/SKILL.md) cubre clasificación, temas, maquetación y el PDF adjunto.
- [manejo-de-secretos](.agents/skills/manejo-de-secretos/SKILL.md) cubre la configuración y las pruebas de RF17.
- [orquestador-pizarra-snap](.agents/skills/orquestador-pizarra-snap/SKILL.md) coordina tareas que abarcan varios módulos o cuya ruta de trabajo todavía hay que determinar. Para una tarea acotada, usá el procedimiento específico o una revisión directa.
