# Requerimientos — Pizarra Snap

Conservamos el catálogo elaborado por Daniela Ferranti en el [commit `96ce561`](https://github.com/nicodf91/pizarra-snap/commit/96ce561c5350a9b9620eb133b42c433e81ed10b3). Los RF se agrupan por aporte original y los RNF describen objetivos de diseño.

> Para el estado de avance de cada requerimiento, ver [`PLAN_TRABAJO_PIZARRA_SNAP.md`](../PLAN_TRABAJO_PIZARRA_SNAP.md).

---

## Requerimientos Funcionales

### Módulo de Nicolás — RF01 a RF05

| RF | Descripción |
|---|---|
| RF01 | Lectura de video de pizarra. El MVP recibe un MP4 pregrabado. La cámara en vivo queda fuera del alcance validado. |
| RF02 | Procesamiento de frames: divide el video en frames individuales para analizarlos. |
| RF03 | Definición de regiones de interés (ROI): tres zonas — Captura Normal, Concepto Importante, Fin de Tema. |
| RF04 | Análisis de histogramas: calcula el histograma de cada ROI y lo compara con su estado habitual. |
| RF05 | Detección de cambios: detecta cuándo una región es cubierta o modificada visualmente. |

### Módulo de Diego — RF06 a RF09

| RF | Descripción |
|---|---|
| RF06 | Identificación del comando: genera el evento correspondiente (`CAPTURA_NORMAL`, `CONCEPTO_IMPORTANTE`, `FIN_DE_TEMA`) según la ROI activada. |
| RF07 | Validación de la acción: reconoce la secuencia `visible → cubierta → visible` para confirmar un comando cuando cumple los criterios de duración y activación. |
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

### Interfaz web — RF17

| RF | Descripción |
|---|---|
| RF17 | Envío del reporte por email (opcional): desde la interfaz, el usuario puede recibir por correo el PDF ya generado, sin volver a procesar el video. Requiere una cuenta emisora configurada en un archivo local de secretos; sin esa configuración, la opción queda desactivada y la descarga sigue disponible. El PDF pasa por el servidor de correo del proveedor, por lo que este envío es una excepción al procesamiento local (RNF08) y solo ocurre si el usuario lo solicita. |

---

## Requerimientos No Funcionales

| RNF | Descripción |
|---|---|
| RNF01 | Facilidad de uso: el sistema debe poder usarse sin conocimientos técnicos. |
| RNF02 | Comandos visuales durante la grabación de la clase. La carga del MP4 y la descarga del reporte se realizan en la interfaz. |
| RNF03 | Tiempo de respuesta como objetivo de diseño. En el MVP el procesamiento comienza al elegir **Generar PDF** después de cargar el video. |
| RNF04 | Confiabilidad: minimizar capturas accidentales. |
| RNF05 | Calidad visual: las imágenes seleccionadas deben permitir leer el contenido de la pizarra. |
| RNF06 | Modularidad: desarrollo en módulos independientes, para facilitar mejoras futuras. |
| RNF07 | Capacidad de evolución. OCR, reconocimiento de contenido, resúmenes y cámara en vivo se plantearon como posibles extensiones. |
| RNF08 | Procesamiento local o controlado. La app local guarda el video en un directorio temporal durante la ejecución. |

---

## Referencias

- Estado de avance por módulo: [`PLAN_TRABAJO_PIZARRA_SNAP.md`](../PLAN_TRABAJO_PIZARRA_SNAP.md)
- Flujo técnico completo: [arquitectura funcional en el plan de trabajo](../PLAN_TRABAJO_PIZARRA_SNAP.md#arquitectura-funcional-y-decisiones-consolidadas)
