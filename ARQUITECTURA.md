La arquitectura técnica de **Pizarra Snap** está estructurada como un pipeline lineal de visión por computadora y procesamiento de documentos, diseñado para asistir a docentes mediante la captura inteligente del pizarrón. El sistema opera bajo una premisa fundamental: trabaja exclusivamente con **frames posteriores al evento** de cobertura (no utiliza un buffer retrospectivo en el flujo principal), lo que permite un procesamiento ágil y estructurado en cinco fases clave:

### 1. Ingesta de Video y Preprocesamiento Visual (Nicolás: RF01–RF05)
El pipeline inicia con la carga y apertura del archivo de video MP4 mediante OpenCV, obteniendo sus propiedades reales (resolución de 1920×1080 píxeles y tasa de FPS real). 
* **Definición de ROIs:** Se definen tres Regiones de Interés (ROI) fijas en forma de recortes rectangulares (slicing de matrices NumPy), correspondientes a cada comando.
* **Análisis de Histogramas:** Cada ROI se convierte a escala de grises, se le aplica un filtro Gaussian Blur de 5x5 para reducir ruido y se calcula su histograma de 256 niveles normalizado con norma L1.
* **Detección de Cobertura:** Mediante la **distancia de Bhattacharyya**, se compara cuantitativamente el histograma actual con uno de referencia "limpio" obtenido al inicio del video. Si la distancia supera el umbral experimental de 0.40, la zona se clasifica de forma transitoria como **CUBIERTA**; de lo contrario, permanece **LIBRE**.

### 2. Máquina de Estados y Recolección de Candidatos (Diego: RF06–RF09)
Esta fase transforma las señales brutas en comandos válidos y gestiona la captura temporal de imágenes.
* **Validación de Intencionalidad:** Para evitar falsos positivos (como cuando el profesor simplemente pasa cerca o escribe tapando varias zonas), el sistema exige la secuencia `LIBRE ➡️ CUBIERTA ➡️ LIBRE` de **una sola ROI a la vez** y con una duración de cobertura de entre 0.5 y 4 segundos.
* **Ventana Temporal Posterior:** Al confirmarse un evento válido, se abre inmediatamente una ventana temporal de captura de **2 segundos**, calculando el número exacto de cuadros a recolectar según los FPS reales (ej. `int(2.0 * fps)`).
* **Contrato en Memoria:** Se leen de corrido y se copian los frames completos de esa ventana, agrupándolos en una estructura de datos liviana en memoria (`capturas`), que contiene el tipo de evento, el momento del video y la lista ordenada de `frames_candidatos`.

### 3. Evaluación de Calidad y Optimización de Memoria (Walter: RF10–RF12 y RF15)
Recibe la lista de candidatos de la fase anterior sin reposicionar ni volver a leer el video.
* **Métricas de Calidad:** Para cada frame candidato se calculan métricas escalares de **nitidez** (varianza del Laplaciano sobre una escala de grises reducida), **contraste** (desviación estándar de intensidades), **movimiento** (diferencia absoluta media con el cuadro previo) y **estabilidad**.
* **Fórmula de Selección (Score):** Se elige un único cuadro ganador mediante una ponderación heurística de **55% nitidez, 30% estabilidad y 15% contraste**, resolviendo empates de manera determinista.
* **Mejora de Imagen Opcional (CLAHE):** Se evalúa una copia en grises con CLAHE. Se conserva una versión procesada de forma paralela únicamente si el contraste mejora al menos 5% y retiene el 90% de la nitidez; la imagen original nítida de la pizarra **nunca** se descarta.
* **Liberación de Memoria:** Tras guardar la imagen original en disco (en formato PNG), Walter **vacía la lista de frames candidatos** pesados en memoria, transfiriendo a Daniela solo un contrato ligero de rutas absolutas (`resultados_walter`).

### 4. Clasificación y Estructuración Temática (Daniela: RF13–RF14)
* **Contrato Liviano:** Daniela recibe las rutas de disco y mapea las identidades de eventos (`CAPTURA_NORMAL`, `CONCEPTO_IMPORTANTE`, `FIN_DE_TEMA`) a sus respectivas categorías visuales. Prioriza la ruta procesada (CLAHE) si existe, usando la original como alternativa segura.
* **Organización por Temas:** Preservando el orden temporal estricto del video, agrupa los registros en una lista de `temas`. Los eventos de tipo `FIN_DE_TEMA` cierran la sección actual de contenido y delimitan el inicio de un tema nuevo para la siguiente captura, estructurando la lógica de apuntes.

### 5. Renderizado y Maquetación del Reporte PDF (Daniela: RF16)
* **Composición Visual con ReportLab:** Utilizando ReportLab y Pillow, genera un documento PDF dinámico de forma local. El motor genera los recursos de fondo en un directorio temporal y maqueta el PDF con una portada de marca institucional (UTN - Diplomatura en IA), encabezados, pies de página y un diseño basado en tarjetas A4.
* **Diferenciación de Tarjetas:** Las tarjetas de categorías "Normal" e "Importante" incluyen bordes específicos de color (paleta teal/ámbar) y renglones de notas para el alumno, mientras que las imágenes se ajustan preservando su relación de aspecto. 
* **Validación de Entrega:** El sistema verifica la existencia y tamaño del PDF generado mediante `pypdf` antes de ponerlo a disposición del usuario final para su descarga.
