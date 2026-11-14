# Pizarra Snap

Pizarra Snap convierte un video pregrabado de una pizarra en un PDF organizado por temas. Durante la grabación, el docente activa tres comandos cubriendo brevemente las zonas marcadas en la pizarra.

- **Captura normal** registra el contenido general.
- **Concepto importante** destaca una captura en el reporte.
- **Fin de tema** incluye la captura y cierra el tema en curso.

Cuando la zona vuelve a quedar visible, el sistema reúne una ventana corta de frames y elige el de mejor calidad. Desarrollamos el proyecto para la **Diplomatura en Inteligencia Artificial**.

## Ejecutar con Streamlit

El entorno local usa **Python 3.12** y las versiones de [requirements.txt](requirements.txt). Desde la raíz del repositorio, ejecutá estos comandos en PowerShell.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```

En macOS o Linux, después de crear el entorno, ejecutá los dos últimos comandos con `.venv/bin/python`.

1. Abrí la URL local que muestra Streamlit, normalmente [localhost:8501](http://localhost:8501).
2. Adjuntá un MP4 y elegí **Generar PDF**. Para repetir nuestra prueba, usá el [video oficial](PLAN_TRABAJO_PIZARRA_SNAP.md#12-video-de-prueba).
3. Cuando el reporte esté listo, elegí **Descargar PDF**. La aplicación conserva el PDF durante la sesión y retira el resultado anterior al cambiar de video.

### Envío del PDF por email (opcional)

Debajo del botón **Descargar PDF**, la aplicación permite recibir el reporte por correo sin volver a procesar el video. Para activarlo hace falta una cuenta de Gmail emisora y su *contraseña de aplicación*, que Google genera después de activar la verificación en dos pasos.

1. Copiá `.streamlit/secrets.toml.example` como `.streamlit/secrets.toml`.
2. Completá `usuario` con la dirección de Gmail emisora y `clave` con su contraseña de aplicación.
3. Reiniciá la aplicación.

El archivo `.streamlit/secrets.toml` está en `.gitignore` y no debe subirse al repositorio. Si no está configurado, el campo y el botón de email quedan desactivados y la descarga sigue disponible. Al elegir el envío, el PDF pasa por los servidores de Gmail.

## Alcance y validación

Integramos el MVP en [el PR #5](https://github.com/nicodf91/pizarra-snap/pull/5). Con el video oficial obtuvimos **3 capturas, 1 tema cerrado y un PDF de 3 páginas**. Comprobamos la descarga en Chromium y verificamos el resultado mediante Streamlit AppTest. El [plan de trabajo](PLAN_TRABAJO_PIZARRA_SNAP.md#16-estado-técnico-consolidado) detalla las pruebas.

Las tres regiones de interés están ajustadas al encuadre del video oficial y deben estar libres alrededor del segundo 0,5. Otros encuadres, cambios de iluminación o distinta resolución pueden afectar la detección. El consumo de memoria aumenta con la resolución, la cantidad de frames por segundo y los eventos detectados. Los resultados de la corrida oficial corresponden a ese archivo.

## Google Colab

El [notebook original](notebooks/PizarraSnap.ipynb) sigue disponible como alternativa en Google Colab. El [manual del notebook](notebooks/README.md) conserva los pasos de ejecución y descarga automática con el video oficial.

## Equipo y contribuciones

El equipo activo está formado por **Nicolás, Diego y Daniela**. Walter participó en el desarrollo original. Conservamos sus aportes y la trazabilidad de los cuatro integrantes.

| Integrante | Aporte original |
|---|---|
| Nicolás | RF01–RF05, lectura del video, frames, regiones de interés e histogramas |
| Diego | RF06–RF09, detección y validación de eventos y recolección de candidatos |
| Walter | RF10–RF12 y RF15, evaluación de calidad, selección, guardado y mejora de capturas |
| Daniela | RF13–RF14 y RF16, clasificación, temas y generación del PDF, incluido su diseño visual original |

La [historia de autoría e integración](PLAN_TRABAJO_PIZARRA_SNAP.md#autoría-git-y-responsabilidad-funcional) distingue los aportes originales de los commits que los adaptaron.

## Archivos y documentación

- [app.py](app.py) contiene la interfaz de Streamlit. [pipeline.py](pipeline.py) ejecuta RF01–RF16 y devuelve el PDF y un resumen.
- El [plan de trabajo](PLAN_TRABAJO_PIZARRA_SNAP.md) reúne los contratos entre módulos, el estado técnico y las mejoras pendientes.
- Recuperamos el [catálogo de requerimientos](docs/REQUERIMIENTOS.md) y la [planificación original](docs/GANTT.md) de Daniela.

## Skills para Codex y Claude Code

Las skills son guías de desarrollo. [AGENTS.md](AGENTS.md) reúne las reglas comunes del repositorio. Cada `SKILL.md` describe un procedimiento para una tarea concreta. Los [procedimientos canónicos](.agents/skills/orquestador-pizarra-snap/SKILL.md) viven en `.agents/skills/`. [CLAUDE.md](CLAUDE.md) importa las reglas comunes y los adaptadores de `.claude/skills/` remiten a esos procedimientos.

- **Codex Desktop.** Abrí un chat de Codex desde el checkout que contiene las skills. Buscá `orquestador-pizarra-snap` en el selector de skills del compositor y seleccionala junto con tu pedido. Si no aparece después de cambiar de rama, abrí un chat nuevo desde ese checkout o reiniciá Codex. [Guía de skills de OpenAI](https://learn.chatgpt.com/docs/build-skills).
- **Claude Code.** Iniciá una sesión en la raíz del checkout. Usá `/` para comprobar que aparecen las cuatro skills y `/memory` para revisar las instrucciones del proyecto. Invocá `/orquestador-pizarra-snap` con tu pedido. [Guía de skills](https://code.claude.com/docs/en/skills) · [Instrucciones e importaciones](https://code.claude.com/docs/en/memory).

Para probar ambos clientes, pedí que indiquen en solo lectura qué revisarían para cambiar los renglones del PDF. El orquestador debería elegir `informe-pdf` y consultar `references/diseno-pdf.md` desde su carpeta canónica. La selección por descripción depende del cliente y de la tarea. Las skills guían al asistente y se aplican con los permisos de su sesión.
