# Cronología y Gantt — Pizarra Snap

Conservamos la planificación original de Daniela Ferranti, registrada en el [commit `96ce561`](https://github.com/nicodf91/pizarra-snap/commit/96ce561c5350a9b9620eb133b42c433e81ed10b3). Las diez etapas y sus duraciones son estimaciones de esa planificación.

> Para el estado real de avance de cada etapa, ver [`PLAN_TRABAJO_PIZARRA_SNAP.md`](../PLAN_TRABAJO_PIZARRA_SNAP.md).

---

## Etapas del proyecto

| Etapa | Actividad | Requerimientos | Tiempo estimado |
|---|---|---|---|
| 1 | Video y frames | RF01, RF02 | 1 jornada |
| 2 | Regiones de interés (ROI) | RF03 | 1 jornada |
| 3 | Histogramas | RF04, RF05 | 2 jornadas |
| 4 | Sistema de comandos | RF06, RF07 | 2 jornadas |
| 5 | Ventana de captura posterior | RF08, RF09 | 2 jornadas |
| 6 | Selección del mejor frame | RF10, RF11, RF12 | 3 jornadas |
| 7 | Procesamiento de pizarra | RF15 | 3 jornadas |
| 8 | Organización por temas | RF13, RF14 | 2 jornadas |
| 9 | Generación de PDF | RF16 | 2 jornadas |
| 10 | Pruebas y ajustes | — | 2 jornadas |

**Duración total estimada:** 20 jornadas.

---

## Detalle de actividades por etapa

**Etapa 1 — Video y frames:** cargar video, obtener FPS, obtener resolución, contar frames, visualizar frames.

**Etapa 2 — Regiones de interés:** establecer ROI, visualizar zonas, validar posiciones.

**Etapa 3 — Histogramas:** escala de grises, blur, cálculo de histograma, comparación de histogramas, definición de umbral.

**Etapa 4 — Sistema de comandos:** implementar `CAPTURA_NORMAL`, `CONCEPTO_IMPORTANTE`, `FIN_DE_TEMA`; validar la secuencia visible → cubierta → visible.

**Etapa 5 — Ventana de captura posterior:** detectar que finalizó la acción, esperar que la ROI vuelva a quedar visible, iniciar ventana temporal, almacenar frames posteriores, finalizar la ventana.

**Etapa 6 — Selección de mejor imagen:** analizar nitidez, movimiento, contraste y estabilidad; seleccionar y guardar automáticamente el mejor frame.

**Etapa 7 — Procesamiento de pizarra.** La planificación consideraba bordes, recorte, perspectiva y limpieza. La implementación de RF15 usa escala de grises y CLAHE de forma opcional, conservando la captura original.

**Etapa 8 — Organización de contenido:** clasificar capturas, crear estructura de temas, destacar conceptos importantes.

**Etapa 9 — Generación de PDF:** generar reporte, agregar imágenes, separar temas, destacar conceptos.

**Etapa 10 — Pruebas previstas.** Prueba integral, detección de errores, calibración de histogramas, pruebas con iluminación diferente, verificación de falsos positivos, ajuste de la duración de la ventana temporal.

---

## Diagrama de Gantt (representación simplificada)

```text
ETAPA                              1  2  3  4  5  6  7  8  9 10

Video y frames                     █

ROI                                   █

Histogramas                            █  █

Comandos                                    █  █

Captura posterior                              █  █

Selección mejor frame                              █  █  █

Procesamiento pizarra                                  █  █  █

Organización                                                 █  █

PDF                                                            █  █

Pruebas finales                                                      █  █
```

---

## Referencias

- Estado de avance por módulo: [`PLAN_TRABAJO_PIZARRA_SNAP.md`](../PLAN_TRABAJO_PIZARRA_SNAP.md)
- Catálogo de requerimientos: [`REQUERIMIENTOS.md`](./REQUERIMIENTOS.md)
