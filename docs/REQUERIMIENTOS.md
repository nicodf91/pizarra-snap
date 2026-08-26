# Requerimientos — Pizarra Snap

Este documento detalla los requerimientos funcionales (RF) y no funcionales (RNF) del proyecto: qué debe hacer el sistema, organizados por módulo.

> Para el estado de avance de cada requerimiento, ver [`PLAN_TRABAJO_PIZARRA_SNAP.md`](../PLAN_TRABAJO_PIZARRA_SNAP.md).

---

## Requerimientos Funcionales

### Módulo de Nicolás — RF01 a RF05

| RF | Descripción |
|---|---|
| RF01 | Lectura de video: el sistema recibe y procesa un video desde cámara o archivo. |
| RF02 | Procesamiento de frames: divide el video en frames individuales para analizarlos. |
| RF03 | Definición de regiones de interés (ROI): tres zonas — Captura Normal, Concepto Importante, Fin de Tema. |
| RF04 | Análisis de histogramas: calcula el histograma de cada ROI y lo compara con su estado habitual. |
| RF05 | Detección de cambios: detecta cuándo una región es cubierta o modificada visualmente. |

### Módulo de Diego — RF06 a RF09

| RF | Descripción |
|---|---|
| RF06 | Identificación del comando: genera el evento correspondiente (`CAPTURA_NORMAL`, `CONCEPTO_IMPORTANTE`, `FIN_DE_TEMA`) según la ROI activada. |
| RF07 | Validación de la acción: reconoce la secuencia `visible → cubierta → visible` para confirmar una acción intencional. |
| RF08 | Ventana temporal de captura: inicia una ventana breve tras el evento validado, almacenando frames posteriores. |
| RF09 | Captura posterior al evento: obtiene y almacena los frames de esa ventana como candidatos. |

### Módulo de Walter — RF10, RF11, RF12 y RF15

| RF | Descripción |
|---|---|
| RF10 | Evaluación de calidad: calcula nitidez, estabilidad, movimiento y contraste de cada frame candidato. |
| RF11 | Selección del mejor frame: elige automáticamente el candidato de mayor calidad. |
| RF12 | Guardado de captura: almacena el frame seleccionado como archivo de imagen. |
| RF15 | Procesamiento de imagen: mejora opcional (CLAHE) solo cuando aporta valor real; conserva siempre el original. |

### Módulo de Daniela — RF13, RF14 y RF16

| RF | Descripción |
|---|---|
| RF13 | Clasificación de captura: asocia cada captura con su categoría (`NORMAL`, `IMPORTANTE`, `FIN_DE_TEMA`). |
| RF14 | Organización por temas: agrupa las capturas en bloques temáticos, delimitados por `FIN_DE_TEMA`. |
| RF16 | Generación de reporte PDF: genera el documento final con identidad visual, organizado por tema. |

---

## Requerimientos No Funcionales

| RNF | Descripción |
|---|---|
| RNF01 | Facilidad de uso: el sistema debe poder usarse sin conocimientos técnicos. |
| RNF02 | Interacción no invasiva: no requiere teclado, mouse, contacto con la computadora ni comandos de voz. |
| RNF03 | Tiempo de respuesta: la detección y selección de imagen deben ser lo suficientemente rápidas para no interrumpir la clase. |
| RNF04 | Confiabilidad: minimizar capturas accidentales. |
| RNF05 | Calidad visual: las imágenes seleccionadas deben permitir leer el contenido de la pizarra. |
| RNF06 | Modularidad: desarrollo en módulos independientes, para facilitar mejoras futuras. |
| RNF07 | Escalabilidad: la arquitectura debe permitir incorporar a futuro OCR, IA, reconocimiento de contenido, resúmenes automáticos y cámaras en tiempo real. |
| RNF08 | Privacidad: procesamiento local o controlado; no se requiere almacenar el video completo de forma permanente. |

---

## Referencias

- Estado de avance por módulo: [`PLAN_TRABAJO_PIZARRA_SNAP.md`](../PLAN_TRABAJO_PIZARRA_SNAP.md)
- Flujo técnico completo: [`ARQUITECTURA.md`](./ARQUITECTURA.md)
