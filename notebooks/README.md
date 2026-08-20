# Notebooks

Esta carpeta contiene el notebook oficial de **Pizarra Snap**:

- [`PizarraSnap.ipynb`](PizarraSnap.ipynb)

## Ejecución en Google Colab

1. Abrir `PizarraSnap.ipynb` en Google Colab.
2. Seleccionar **Runtime → Run all**.
3. Cuando se solicite, elegir únicamente `proyecto_pizzarasnap.mp4`.
4. Esperar el procesamiento completo del video.
5. Obtener el PDF final mediante la celda opcional de descarga ubicada al final del notebook.

El PDF se genera actualmente en:

```text
/tmp/pizarra_snap_reportes/reporte_pizarra_snap_real.pdf
```

La descarga se mantiene fuera de `generar_pdf_clase`: RF16 sólo genera y valida el archivo, mientras que la última celda integra opcionalmente la descarga de Colab.

## Dependencias

Colab ya incluye OpenCV, NumPy y Matplotlib. El notebook instala ReportLab, Pillow y pypdf antes de generar y validar el reporte.

## Regla de trabajo

Antes de modificar el notebook, consultar [`../README.md`](../README.md) y [`../PLAN_TRABAJO_PIZARRA_SNAP.md`](../PLAN_TRABAJO_PIZARRA_SNAP.md). Los cambios deben realizarse desde una rama de trabajo y revisarse antes de integrar a `main`.
