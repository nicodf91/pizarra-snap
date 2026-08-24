El flujo de trabajo en **Pizarra Snap** está estructurado como una secuencia lineal de dependencias estrictas, donde cada módulo se ejecuta a partir de la salida validada del anterior, evitando la duplicación de procesos (como reabrir el video o recalcular datos). 

A continuación se detalla la cadena de dependencias entre los integrantes y sus respectivos requerimientos funcionales (RF):

### 1. Nicolás (RF01–RF05) ➡️ Diego (RF06–RF09)
* **Lo que se entrega:** Coordenadas de las tres Regiones de Interés (ROI), histogramas normalizados de referencia y la señal de estado **LIBRE/CUBIERTA** basada en la distancia de Bhattacharyya.
* **Dependencia:** Diego requiere esta señal de cambio visual para poder asociar las ROI activadas con un comando específico y validar que la acción sea intencional.

### 2. Diego (RF06–RF09) ➡️ Walter (RF10, RF11, RF12, RF15)
* **Lo que se entrega:** La estructura `capturas`, que contiene el tipo de evento confirmado, el momento en que ocurrió y una lista de **frames candidatos** (imágenes completas sin procesar extraídas durante la ventana temporal de ~2 segundos posterior al evento).
* **Dependencia:** Walter depende de este conjunto de frames posteriores para evaluar la calidad visual (nitidez, contraste, estabilidad) y elegir el mejor cuadro, sin necesidad de reposicionar ni volver a leer el archivo de video.



### 3. Walter (RF10, RF11, RF12, RF15) ➡️ Daniela - RF13
* **Lo que se entrega:** El objeto `resultados_walter`.

Este objeto de datos que contiene la siguiente información:
*   La **identidad del evento** y el tipo de comando detectado.
*   Las **rutas absolutas en el disco** donde se guardaron las capturas originales en formato PNG (`captura_path`).
*   Las **rutas de las capturas mejoradas con CLAHE** (`captura_procesada_path`), que tendrán el valor `None` si la imagen original no requirió o no superó los filtros de mejora visual.
*   Las **métricas de evaluación** del frame ganador.


    Este intercambio es muy eficiente en términos de memoria. Walter almacena las imágenes de manera física y **vacía la lista de frames candidatos** de la memoria. Al entregarle únicamente las rutas absolutas y la metadata a Daniela, se evita la duplicación y transferencia de frames completos (matrices de píxeles pesadas), permitiendo que Daniela clasifique y agrupe los temas en el requerimiento RF13 de manera sumamente ágil.

* **Dependencia:** Daniela (en RF13) requiere estas rutas persistidas de las imágenes físicas para realizar una clasificación de categorías y crear un contrato liviano (`resultados_reporte`) en lugar de arrastrar frames completos en memoria.


### 4. Daniela: RF13 ➡️ RF14 (Organización por temas)
* **Lo que se entrega:** Los registros de capturas ya clasificados (`resultados_reporte`), que conservan la identidad del evento, momento y la ruta física final seleccionada.

* **Dependencia:** RF14 depende de esta lista ordenada de registros livianos para agrupar las capturas en bloques temáticos, utilizando los eventos `FIN_DE_TEMA` para delimitar y cerrar cada sección.

### 5. Daniela: RF14 ➡️ RF16 (Generación del reporte PDF)
* **Lo que se entrega:** Una lista estructurada de **`temas`** que contiene las capturas organizadas en secuencia lineal.
* **Dependencia:** RF16 utiliza esta estructura temática para maquetar el documento con ReportLab, dibujando la portada, las tarjetas correspondientes a cada categoría y los renglones de notas. Finalmente, valida la existencia y tamaño del PDF para entregarlo al usuario.








