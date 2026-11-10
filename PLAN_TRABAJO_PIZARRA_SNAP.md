# Pizarra Snap — Plan de trabajo colaborativo

El equipo activo está formado por **Nicolás, Diego y Daniela**. Walter participó en el desarrollo original. El registro de [autoría y responsabilidad funcional](#autoría-git-y-responsabilidad-funcional) conserva las contribuciones de los cuatro integrantes.

Actualizado el 10/11/2026.

---

## Índice

- [1. Objetivo y alcance](#1-objetivo-y-alcance)
- [2. Estado consolidado y criterio general](#2-estado-consolidado-y-criterio-general)
  - [Arquitectura funcional y decisiones consolidadas](#arquitectura-funcional-y-decisiones-consolidadas)
- [3. Convención de estados](#3-convención-de-estados)
- [4. Matriz maestra RF01–RF16](#4-matriz-maestra-rf01rf16)
- [5. Módulo de Nicolás — RF01 a RF05](#5-módulo-de-nicolás--rf01-a-rf05)
- [6. Módulo de Diego — RF06 a RF09](#6-módulo-de-diego--rf06-a-rf09)
- [7. Módulo de Walter — RF10, RF11, RF12 y RF15](#7-módulo-de-walter--rf10-rf11-rf12-y-rf15)
- [8. Módulo de Daniela — RF13, RF14 y RF16](#8-módulo-de-daniela--rf13-rf14-y-rf16)
- [9. Contratos y flujo entre integrantes](#9-contratos-y-flujo-entre-integrantes)
- [10. Revisión cruzada](#10-revisión-cruzada)
- [11. Organización actual del repositorio](#11-organización-actual-del-repositorio)
- [12. Video de prueba](#12-video-de-prueba)
- [13. Historia y criterio de trabajo con GitHub](#13-historia-y-criterio-de-trabajo-con-github)
- [14. Regla importante para el notebook](#14-regla-importante-para-el-notebook)
- [15. Checklist de consolidación completado](#15-checklist-de-consolidación-completado)
- [16. Estado técnico consolidado](#16-estado-técnico-consolidado)
- [17. Historia de integración](#17-historia-de-integración)
- [18. Criterio para actualizar este documento](#18-criterio-para-actualizar-este-documento)
- [19. Limitaciones vigentes](#19-limitaciones-vigentes)
- [20. Deuda técnica y mejoras futuras](#20-deuda-técnica-y-mejoras-futuras)
- [21. Glosario](#21-glosario)
- [22. Próximos pasos](#22-próximos-pasos)

---

## 1. Objetivo y alcance

Pizarra Snap es un sistema de visión por computadora pensado para asistir a docentes durante una clase presencial.

Una cámara fija observa la pizarra. El docente puede generar tres tipos de eventos cubriendo brevemente una zona visual con un elemento cotidiano, como el borrador:

- 📸 **CAPTURA NORMAL**
- ⭐ **CONCEPTO IMPORTANTE**
- 📌 **FIN DE TEMA**

El sistema detecta visualmente el evento, espera a que la zona vuelva a quedar visible y analiza una breve secuencia de frames **posteriores** a la acción para seleccionar la mejor imagen. Las capturas se clasifican y posteriormente se utilizan para generar un reporte PDF organizado por temas.

> La arquitectura vigente trabaja con frames **posteriores al evento**. No se utiliza un buffer retrospectivo como parte del flujo principal.

El alcance validado es un MP4 pregrabado con cámara fija. La interfaz local permite cargar el video, generar el PDF y descargarlo.

---

## 2. Estado consolidado y criterio general

Integramos el MVP de Streamlit en `main` con el [PR #5](https://github.com/nicodf91/pizarra-snap/pull/5), en el commit [`c073fac`](https://github.com/nicodf91/pizarra-snap/commit/c073fac2486e3d81865ca205876e2f42c6c0fc30). La [aplicación local](README.md#ejecutar-con-streamlit) reutiliza RF01–RF16 y conserva los algoritmos y el diseño del PDF.

[app.py](app.py) recibe un MP4 y lo copia por bloques a un directorio temporal propio de cada ejecución. [pipeline.py](pipeline.py) recibe la ruta del video y ese directorio de trabajo. La función `procesar_video()` devuelve la ruta del PDF y un resumen sin imágenes. La interfaz conserva el PDF en la sesión para descargarlo sin volver a procesar el video. Si se adjunta otro archivo, retira el resultado anterior.

El [notebook original](notebooks/PizarraSnap.ipynb) conserva el hash Git `583c2db6bb67f59db5d6df5155a1686ce12ee221` y sigue siendo una alternativa funcional en [Google Colab](notebooks/README.md). Las [pruebas del MVP](#16-estado-técnico-consolidado) compararon el módulo local con el flujo original.

### Arquitectura funcional y decisiones consolidadas

```text
VIDEO → ROI E HISTOGRAMAS → EVENTOS → CANDIDATOS
      → CALIDAD Y PNG → CATEGORÍAS Y TEMAS → PDF
```

| Decisión | Significado en Pizarra Snap |
|---|---|
| Ventana posterior | RF08/RF09 recolectan frames después de confirmar el evento; el flujo principal no usa un buffer retrospectivo |
| Detección visual | RF03–RF05 utilizan ROI fijas, histogramas y distancia de Bhattacharyya con umbral `0.40` |
| Contrato en memoria | La etapa de selección recibe los candidatos de RF09 sin volver a abrir ni reposicionar el video |
| Selección relativa | RF10 compara nitidez, estabilidad y contraste dentro de cada evento con pesos 55/30/15 |
| Original preservada | RF12 guarda el ganador; RF15 conserva CLAHE sólo cuando mejora las métricas y nunca reemplaza la original |
| Contrato liviano | RF13 entrega identidades y rutas a RF14/RF16 en lugar de duplicar frames completos |
| Generación y descarga separadas | RF16 genera el PDF. La app ofrece una descarga desde la sesión y la última celda del notebook inicia la descarga en Colab |
| Entornos | Python 3.12 y Streamlit para la aplicación local. Google Colab para ejecutar el notebook original |

### Criterio general de trabajo

El proyecto se divide siguiendo los requerimientos funcionales RF01–RF16.

Durante la integración, cada módulo siguió estos criterios:

1. partir del resultado validado del módulo anterior;
2. mantener el código comentado de manera breve, clara y didáctica;
3. conservar las variables y nombres acordados siempre que sea posible;
4. evitar modificar datos originales cuando se pueda trabajar sobre copias;
5. incluir al menos una prueba que permita verificar el funcionamiento;
6. dejar documentado qué entrada recibe y qué salida entrega al siguiente módulo;
7. actualizar este archivo cuando el módulo cambie de estado;
8. integrarse a `main` solamente después de una revisión.

---

## 3. Convención de estados

| Estado | Significado |
|---|---|
| ✅ VALIDADO | Implementado y verificado mediante pruebas de integración |
| 🟡 VALIDADO CON LIMITACIÓN | Funciona para el alcance validado y conserva una limitación documentada |
| ✅ REALIZADO | Código implementado y validado por el responsable |
| 🟡 EN PROGRESO | El integrante está trabajando en el módulo |
| ⬜ PENDIENTE | Trabajo aún no iniciado |
| 🔁 EN REVISIÓN | Implementado y pendiente de revisión cruzada antes de integrar |
| ⚠️ AJUSTE | Funciona, pero requiere calibración o mejora |

---

# 4. Matriz maestra RF01–RF16

| RF | Autoría funcional original | Objetivo | Entrada | Proceso | Salida | Dependencia anterior | Entrega a | Estado | Limitación |
|---|---|---|---|---|---|---|---|---|---|
| RF01 | Nicolás | Cargar y abrir el video | MP4 seleccionado | Carga desde la interfaz o Colab y apertura con `cv2.VideoCapture` | Video y propiedades del archivo | — | RF02 | ✅ VALIDADO | El MP4 debe poder decodificarse |
| RF02 | Nicolás | Leer y comprender frames | Video abierto | Lectura BGR y análisis NumPy | Frame y propiedades de píxel | RF01 | RF03 | ✅ VALIDADO | Depende de una lectura válida |
| RF03 | Nicolás | Definir las tres ROI | Frame completo | Coordenadas y slicing | Tres ROI y sus coordenadas | RF02 | RF04 | ✅ VALIDADO | ROI fijas para cámara y resolución actuales |
| RF04 | Nicolás | Representar visualmente cada ROI | ROI BGR | Gris, Gaussian Blur, histograma y L1 | Histograma normalizado | RF03 | RF05 | ✅ VALIDADO | El histograma no conserva posición espacial |
| RF05 | Nicolás | Detectar cambios | Histograma actual y referencia | Distancia de Bhattacharyya + umbral | Distancia y `LIBRE/CUBIERTA` | RF04 | RF06 | 🟡 VALIDADO CON LIMITACIÓN | Umbral `0.40` dependiente del escenario |
| RF06 | Diego | Identificar el comando | Estado de las ROI | Mapping de ROI a evento | Tipo de evento | RF05 | RF07 | ✅ VALIDADO | Requiere distinguir una ROI activa |
| RF07 | Diego | Validar la acción | Transiciones de estado | `LIBRE → CUBIERTA → LIBRE`, duración y exclusividad | Evento confirmado + momento | RF06 | RF08 | ✅ VALIDADO | Cobertura válida entre 0,5 s y 4 s |
| RF08 | Diego | Abrir la ventana posterior | Evento confirmado y FPS | `int(2.0 * fps)` | Ventana de captura | RF07 | RF09 | ✅ VALIDADO | Duración aproximada por truncamiento |
| RF09 | Diego | Recolectar candidatos | Frames posteriores | Copia de frames completos | `capturas` con `frames_candidatos` | RF08 | RF10 | 🟡 VALIDADO CON LIMITACIÓN | Consumo elevado de memoria |
| RF10 | Walter | Evaluar calidad | Lista de candidatos | Nitidez, contraste, movimiento y estabilidad | Evaluaciones y score | RF09 | RF11 | ✅ VALIDADO | Pesos heurísticos 55/30/15 |
| RF11 | Walter | Elegir el mejor frame | Evaluaciones y candidatos | Máximo score y desempates deterministas | Ganador, índice y métricas | RF10 | RF12/RF15 | ✅ VALIDADO | Selección visual, no semántica |
| RF12 | Walter | Guardar la captura | Frame ganador y destino | `cv2.imwrite` con validación | PNG original y ruta absoluta | RF11 | RF13 | ✅ VALIDADO | Depende del filesystem de la sesión |
| RF13 | Daniela | Clasificar y aligerar el contrato | `resultados_walter` | Mapping de evento y selección de ruta | `resultados_reporte` | RF12/RF15 | RF14 | ✅ VALIDADO | Fallback con margen de robustez futura |
| RF14 | Daniela | Organizar por temas | Registros ordenados | Agrupación y cierre por `FIN_DE_TEMA` | Lista de temas | RF13 | RF16 | ✅ VALIDADO | Depende del orden de eventos |
| RF15 | Walter | Mejorar opcionalmente | Frame ganador BGR | Gris + CLAHE con criterios medibles | Procesada o `None` + evaluación | RF11 | RF13 | ✅ VALIDADO | Umbrales heurísticos; original preservada |
| RF16 | Daniela | Generar el reporte | Temas, destino y datos de portada | Validación, maquetación ReportLab y apertura con pypdf | `Path` del PDF | RF14 | Usuario | ✅ VALIDADO | Páginas variables según las capturas y los temas |

---

# 5. Módulo de Nicolás — RF01 a RF05

## Estado

```text
RF01 ✅ VALIDADO
RF02 ✅ VALIDADO
RF03 ✅ VALIDADO
RF04 ✅ VALIDADO
RF05 🟡 VALIDADO CON LIMITACIÓN
```

## Objetivo general del módulo

Construir la base de visión por computadora del proyecto: leer el video, trabajar con sus frames, definir las tres ROI y transformar esas regiones en señales capaces de indicar si una zona está libre o cubierta.

### Contribución consolidada

- **Aporte:** Nicolás desarrolló RF01–RF05: carga de video, análisis de frames, ROI, histogramas, distancia de Bhattacharyya y estados `LIBRE/CUBIERTA`.
- **Qué funcionó:** las coordenadas y el umbral experimental separaron correctamente los casos libres, transiciones y coberturas claras del video oficial.
- **Desafío de integración:** las referencias libres utilizadas durante la exploración provenían de segundos elegidos manualmente.
- **Adaptación necesaria:** para el recorrido continuo, Diego calculó referencias limpias comunes al inicio del video sin reemplazar las funciones de Nicolás.
- **Resultado final:** RF05 entrega la señal visual que permite identificar y validar los tres comandos.

---

## RF01 — Lectura de video

### Trabajo original en Colab

- Se creó el notebook principal en Google Colab.
- Se cargaron las librerías iniciales:
  - OpenCV;
  - NumPy;
  - Matplotlib;
  - herramientas de archivos de Google Colab.
- Se cargó el video de prueba `proyecto_pizzarasnap.mp4`.
- Se abrió correctamente mediante `cv2.VideoCapture()`.
- Se validó la apertura mediante `video.isOpened()`.
- Se obtuvieron las propiedades reales del archivo.

### Datos obtenidos

- Resolución: **1920 × 1080**
- FPS informado por OpenCV: **28.843967150979154**
- Cantidad de frames: **1522**
- Duración aproximada: **52.77 segundos**

### Salida hacia RF02

Objeto de video abierto correctamente y disponible para lectura frame por frame.

---

## RF02 — Procesamiento de frames

### Trabajo realizado

- Se posicionó el video en el frame inicial.
- Se leyó correctamente el primer frame mediante `video.read()`.
- Se verificó que el frame es un `numpy.ndarray`.
- Se analizaron:
  - `shape`;
  - alto;
  - ancho;
  - canales;
  - `dtype`;
  - valores BGR de un píxel.
- Se convirtió el frame de BGR a RGB para visualizarlo con Matplotlib.
- Se mostraron las coordenadas X/Y sobre la imagen.
- Se relacionó el frame con conceptos trabajados en la Diplomatura:
  - matrices;
  - NumPy;
  - `shape`;
  - píxeles;
  - bits y `uint8`;
  - canales BGR;
  - slicing.

### Resultado validado

```text
Tipo de frame: numpy.ndarray
Shape: (1080, 1920, 3)
dtype: uint8
```

Ejemplo de píxel analizado:

```text
B = 142
G = 144
R = 126
```

### Salida hacia RF03

Frame completo disponible como matriz NumPy de 1080 × 1920 × 3.

---

## RF03 — Regiones de interés (ROI)

### Trabajo realizado

Se definieron y visualizaron las tres zonas que actuarán como comandos visuales.

### Coordenadas acordadas

#### 📸 ROI — Captura normal

```python
x1_normal, x2_normal = 75, 210
y1_normal, y2_normal = 190, 300
```

Shape obtenido:

```text
(110, 135, 3)
```

#### ⭐ ROI — Concepto importante

```python
x1_importante, x2_importante = 75, 210
y1_importante, y2_importante = 400, 510
```

Shape obtenido:

```text
(110, 135, 3)
```

#### 📌 ROI — Fin de tema

```python
x1_fin, x2_fin = 75, 215
y1_fin, y2_fin = 585, 740
```

Shape obtenido:

```text
(155, 140, 3)
```

### Validaciones realizadas

- Las ROI fueron dibujadas sobre una copia del frame.
- Se verificó visualmente que cada región encierra correctamente su símbolo.
- Las tres regiones fueron recortadas mediante slicing de NumPy.
- Se visualizaron individualmente las tres imágenes recortadas.

### Nota de continuidad

Las coordenadas se mantuvieron **válidas durante las pruebas de RF04/RF05** y no fue necesario modificar su tamaño para el video de prueba actual.

### Base disponible para RF04/RF05

- video correctamente abierto;
- frames accesibles;
- frame base validado;
- coordenadas de las tres ROI;
- variables `roi_normal`, `roi_importante` y `roi_fin`.

---

## RF04 — Análisis de histogramas

### Estado

**✅ REALIZADO**

### Trabajo realizado

- Se convirtió cada ROI de BGR a escala de grises mediante `cv2.cvtColor()`.
- Se aplicó `GaussianBlur` con kernel `5 × 5` para reducir pequeñas variaciones y ruido sin perder la forma general de los símbolos.
- Se calcularon histogramas de 256 niveles de intensidad mediante `cv2.calcHist()`.
- Se normalizaron los histogramas con norma L1 mediante `cv2.normalize()` para comparar distribuciones independientemente del tamaño de cada ROI.
- Se graficaron y explicaron los histogramas de las tres regiones.
- Se compararon visualmente ejemplos de ROI libre y cubierta.
- Se encapsuló el preprocesamiento y cálculo en la función reutilizable:

```python
calcular_histograma_roi(roi)
```

### Conceptos de la Diplomatura involucrados

- escala de grises;
- kernel;
- convolución;
- Gaussian Blur;
- histogramas;
- normalización;
- arrays NumPy;
- OpenCV;
- Matplotlib.

### Resultado validado

Cada ROI puede transformarse en un histograma normalizado preparado para una comparación cuantitativa.

Las sumas de los histogramas normalizados quedaron aproximadamente en `1.0`, con pequeñas diferencias atribuibles a precisión de punto flotante.

### Salida hacia RF05

Histograma normalizado de cada ROI listo para comparar el estado actual con un estado libre de referencia.

---

## RF05 — Detección de cambios

### Estado

**✅ REALIZADO**

### Trabajo realizado

- Se eligió la **distancia de Bhattacharyya** mediante `cv2.compareHist()` como métrica de comparación.
- Se creó una función para obtener una ROI desde un momento determinado del video:

```python
obtener_roi_en_segundo(...)
```

- Se creó una función para medir la distancia entre el histograma actual y un histograma de referencia:

```python
medir_distancia_roi(...)
```

- Se estableció un umbral experimental:

```python
umbral_cobertura = 0.40
```

- Se creó la clasificación de estado:

```text
distancia < 0.40  → LIBRE
distancia >= 0.40 → CUBIERTA
```

- Se integró la medición y clasificación en:

```python
detectar_estado_roi(...)
```

### Pruebas realizadas

Se evaluaron estados libres, momentos de transición y coberturas claras en las tres ROI.

| ROI | Libre vs. libre | Transición | Cobertura clara |
|---|---:|---:|---:|
| 📸 Captura normal | 0.1117 | 0.2544 | 0.7967 |
| ⭐ Concepto importante | 0.0622 | 0.1747 | 0.8461 |
| 📌 Fin de tema | 0.0824 | 0.1483 | 0.5488 |

También se probó movimiento cercano a la ROI de Captura normal sin una cobertura suficiente, con una distancia aproximada de `0.1767`, que permaneció correctamente como `LIBRE`.

### Prueba automática final

Se utilizaron `assert` para comprobar que:

- los casos libres se clasifican como `LIBRE`;
- las transiciones iniciales permanecen como `LIBRE`;
- las coberturas claras se clasifican como `CUBIERTA`.

La prueba final terminó correctamente con el mensaje:

```text
✅ RF05 validado correctamente.
Las tres ROI distinguen estados LIBRE y CUBIERTA con el umbral experimental.
```

### Limitación conocida

El umbral `0.40` fue calibrado experimentalmente sobre el video de prueba actual. No es un valor universal y puede requerir ajuste si cambian:

- cámara;
- iluminación;
- pizarra;
- tamaño o posición de las ROI.

RF05 detecta un **cambio visual suficiente**, pero no decide por sí solo si la cobertura fue intencional. La validación de la secuencia:

```text
VISIBLE → CUBIERTA → VISIBLE
```

corresponde a RF07.

### Nota de integración sobre las referencias

Durante la calibración se utilizaron momentos libres cercanos a cada evento para medir con precisión la separación entre estados. Para una ejecución continua, el siguiente módulo deberá partir de referencias limpias obtenidas en una inicialización común o en una fase explícita de calibración, evitando depender de segundos elegidos manualmente del video.

### Entrega de Nicolás a Diego

La salida disponible para cada ROI es:

```text
(distancia, estado)
```

con:

```text
estado = LIBRE
o
estado = CUBIERTA
```

Quedan disponibles las coordenadas de las tres ROI y las funciones necesarias para que RF06 pueda asociar cada región con su comando correspondiente.

---

# 6. Módulo de Diego — RF06 a RF09

## Estado

```text
RF06 ✅ VALIDADO
RF07 ✅ VALIDADO
RF08 ✅ VALIDADO
RF09 🟡 VALIDADO CON LIMITACIÓN
```

## Objetivo general del módulo

Convertir los cambios de las ROI en comandos reales, validar que la acción sea intencional y, después del evento confirmado, abrir una ventana temporal para recolectar los frames candidatos.

Esta agrupación mantiene juntas dos etapas fuertemente relacionadas:

```text
DETECTAR COMANDO → VALIDAR EVENTO → ABRIR VENTANA → RECOLECTAR FRAMES
```

### Contribución consolidada

- **Aporte:** Diego implementó RF06–RF09 y sus commits se incorporaron conservando su autoría Git.
- **Qué funcionó:** el recorrido continuo detecta los tres eventos reales, valida duración y exclusividad y obtiene ventanas completas con los FPS reales.
- **Desafío de integración:** la salida debía conectarse con un selector de calidad sin reabrir el video y sin conservar candidatos indefinidamente.
- **Adaptación necesaria:** se formalizó `capturas` como contrato y el módulo de Walter libera cada lista después de guardar el ganador.
- **Resultado final:** cada evento confirmado entrega su tipo, momento y lista ordenada de frames candidatos.

---

## RF06 — Identificación del comando

### Implementación actual

Relacionar cada ROI con su evento:

```text
ROI Captura normal      → CAPTURA_NORMAL
ROI Concepto importante → CONCEPTO_IMPORTANTE
ROI Fin de tema         → FIN_DE_TEMA
```

- Detectar qué zona fue activada.
- Evitar confundir una ROI con otra.
- Guardar el tipo de evento en una variable clara.

### Salida actual

Generar uno de estos eventos:

```text
CAPTURA_NORMAL
CONCEPTO_IMPORTANTE
FIN_DE_TEMA
```

---

## RF07 — Validación de la acción

### Implementación actual

Implementar la secuencia válida:

```text
VISIBLE → CUBIERTA → VISIBLE
```

La acción no debe validarse mientras el símbolo continúe tapado.

La implementación considera:

- duración mínima de la cobertura;
- retorno de la ROI al estado visible;
- bloqueo temporal para evitar duplicados;
- falsos positivos.

### Salida actual

Evento único y validado solamente después de que la zona vuelva a quedar visible.

Variables esperadas o equivalentes:

```text
evento_validado
tipo_evento
momento_del_evento
```

---

## RF08 — Ventana temporal posterior

### Implementación actual

- Comenzar la ventana únicamente después de RF07.
- Trabajar con una duración inicial aproximada de **2 segundos**.
- Calcular cuántos frames corresponden a esa ventana utilizando los FPS reales.
- Tener en cuenta que el video de prueba presenta FPS no entero.
- Evitar depender innecesariamente de un valor fijo de 30 FPS.
- Almacenar solamente los frames candidatos de esa ventana.

### Salida actual

Lista o colección de frames obtenidos después de la activación.

---

## RF09 — Captura posterior al evento

### Implementación actual

- Leer los frames durante la ventana.
- Numerarlos o asociarlos con su posición temporal.
- Guardarlos temporalmente como candidatos.
- Finalizar correctamente la ventana.
- No conservar indefinidamente frames que ya no sean necesarios.

### Salida actual

Conjunto de frames candidatos listo para evaluar la calidad.

### Entrega de Diego a Walter

Diego entrega la estructura:

```text
frames_candidatos
tipo_evento
momento_del_evento
```

### Resultado obtenido (RF06–RF09)

- Las referencias LIBRES de las tres ROI se calculan automáticamente al
  arrancar (`segundo_inicio = 0.5`), en vez de depender de segundos
  elegidos a mano, como pedía la nota de integración de RF05.
- El video se recorre **de corrido** (frame a frame, sin `video.set()`
  repetido), porque saltar a segundos sueltos resultó demasiado lento
  sobre el video completo.
- RF06/RF07 exigen que la transición LIBRE→CUBIERTA sea de **una sola ROI
  a la vez** y que la cobertura dure entre `0.5s` y `4s` para confirmarse
  como comando — esto descarta el ruido detectado durante las pruebas: el
  profesor tapa las tres ROI juntas al acercarse a escribir en la pizarra
  (quedan apiladas en el mismo borde), lo cual no es un comando intencional.
- RF08 calcula la ventana posterior (`ventana_frames = int(2.0 * fps)`)
  usando el fps real del video (28.84), no un valor fijo de 30.
- RF09 entrega `capturas`: una lista de diccionarios, uno por comando
  confirmado, cada uno con `tipo_evento`, `momento_del_evento` y
  `frames_candidatos` (los frames posteriores al evento, sin procesar).

### Prueba automática final

Se utilizó `assert` para comprobar que:

- se detectan exactamente los 3 comandos reales del video de prueba, en
  el orden esperado (`CAPTURA_NORMAL`, `CONCEPTO_IMPORTANTE`,
  `FIN_DE_TEMA`);
- cada captura tiene la ventana completa de frames (`ventana_frames`).

La prueba final terminó correctamente con el mensaje:

```text
✅ RF06-RF09 validado correctamente.
Los tres comandos se detectaron, filtraron y su ventana posterior se recolectó completa.
```

### Limitación conocida

Cada `frames_candidatos` guarda frames completos en memoria, con resolución completa y sin comprimir. Para el video validado:

```text
1920 × 1080 × 3 uint8 = 6.220.800 bytes por frame
171 candidatos simultáneos = 1.063.756.800 bytes ≈ 1.014 MiB
```

Esta estimación abarca solo los candidatos. El módulo de selección vacía cada lista después de guardar el ganador, por lo que las listas se acumulan antes de ese paso. El pico real de memoria también depende del entorno y de las demás etapas.

---

# 7. Módulo de Walter — RF10, RF11, RF12 y RF15

## Estado

**✅ VALIDADO**

## Objetivo

Elegir automáticamente la mejor captura posterior al evento, guardarla y mejorar la imagen de la pizarra cuando una transformación aporte valor real.

### Contribución consolidada

- **Aporte:** Walter aportó nitidez mediante varianza del Laplaciano, contraste, selección de frames y persistencia con `cv2.imwrite`.
- **Qué funcionó:** las métricas permiten comparar candidatos y evitar elegir automáticamente el primer frame disponible.
- **Desafío de integración:** la rama original volvía a posicionar el video y utilizaba cobertura de la ROI, mientras el contrato actual ya entrega frames posteriores al evento.
- **Adaptación necesaria:** la selección consume `frames_candidatos`, agrega estabilidad y usa CLAHE sólo cuando supera criterios medibles.
- **Resultado final:** se conserva una captura original por evento, sus métricas y una versión procesada opcional sin reemplazar la original.

### Recuperación semántica del trabajo previo

Se auditó el notebook de la rama `seleccionFrame` sin unir su historia Git. De Walter se recuperaron:

- la varianza del Laplaciano como medida de nitidez;
- la desviación estándar de intensidades como medida de contraste;
- el guardado mediante `cv2.imwrite` y nombres descriptivos.

Se adaptaron esas ideas al contrato actual de Diego. La implementación ya no vuelve a posicionar ni leer el video y no utiliza la cobertura de la ROI como objetivo de selección: consume directamente los `frames_candidatos` posteriores al evento.

Se descartaron la selección del frame más cubierto, las comparaciones por igualdad exacta de métricas flotantes, las demostraciones con segundos escritos a mano y las dos definiciones duplicadas de `guardar_frame`. Ese enfoque podía favorecer la presencia de la mano y reconstruía una etapa que RF06–RF09 ya resolvieron. La rama auditada tampoco contenía una implementación efectiva de RF15.

---

## RF10 — Evaluación de calidad

Cada candidato produce estas métricas:

- `nitidez`: varianza del Laplaciano sobre una versión gris reducida al 50%;
- `contraste`: desviación estándar de intensidades;
- `movimiento`: diferencia absoluta media respecto del frame anterior;
- `estabilidad`: movimiento normalizado en sentido inverso dentro del evento;
- `score`: combinación relativa de 55% nitidez, 30% estabilidad y 15% contraste.

El primer candidato se compara con su vecino para no premiarlo artificialmente con movimiento cero. Solamente se conservan métricas escalares durante la evaluación.

---

## RF11 — Selección del mejor frame

Se elige exactamente un ganador por evento con el mayor `score`. Los desempates favorecen mayor nitidez, menor movimiento y, finalmente, el candidato más temprano para obtener un resultado determinista.

La comparación temporal penaliza indirectamente la mano o el borrador en movimiento sin introducir un detector de personas. En el video real, los tres ganadores se inspeccionaron visualmente y muestran la pizarra completa, legible y sin mano/borrador.

---

## RF12 — Guardado de captura

La captura original se guarda en PNG, se valida el resultado de `cv2.imwrite` y se conserva una ruta absoluta en `captura_path`.

Los nombres tienen este formato ordenado:

```text
captura_001_captura_normal_<momento_ms>ms.png
```

En Colab las capturas se guardan en `/content/capturas_pizarra_snap`. En el MVP se crean dentro del directorio temporal de cada ejecución y se eliminan cuando termina la generación del reporte.

---

## RF15 — Procesamiento de imagen

Se evalúa una copia en escala de grises con CLAHE (`clipLimit=2.0`, grilla `8 × 8`). Solo se conserva si aumenta el contraste al menos 5% y mantiene al menos 90% de la nitidez medida. La versión original nunca se reemplaza.

En el video real ninguna de las tres capturas superó ambos umbrales; por eso `captura_procesada`, `captura_procesada_path` y `procesamiento_aplicado` quedaron en `None`. La rama sí se validó con una imagen sintética de bajo contraste, donde se generó, guardó y volvió a leer una versión procesada de un solo canal.

No se aplicaron recorte, threshold, Canny, morfología ni corrección de perspectiva porque no existe una geometría validada de la pizarra y no demostraron mejorar estas capturas.

### Contrato de entrada real

```python
{
    "tipo_evento": str,
    "momento_del_evento": float,
    "frames_candidatos": list[np.ndarray],
}
```

### Contrato de salida real

```python
{
    "numero_captura": int,
    "tipo_evento": str,
    "momento_del_evento": float,
    "indice_mejor_frame": int,
    "mejor_frame": np.ndarray,
    "metricas_mejor_frame": dict,
    "evaluaciones_calidad": list[dict],
    "captura_path": str,
    "captura_procesada": np.ndarray | None,
    "captura_procesada_path": str | None,
    "procesamiento_aplicado": str | None,
    "evaluacion_procesamiento": dict,
}
```

Después de guardar cada resultado se vacía la lista `frames_candidatos` correspondiente, conservando solamente el ganador y la eventual versión procesada. Esto reduce la presión de memoria sin refactorizar RF09.

### Pruebas ejecutadas

- casos sintéticos nítido/desenfocado y estable/en movimiento;
- guardado, existencia y lectura válida con OpenCV;
- generación opcional RF15 sobre bajo contraste y preservación de la original;
- ejecución real completa: `CAPTURA_NORMAL`, `CONCEPTO_IMPORTANTE`, `FIN_DE_TEMA`, en ese orden, con 57 candidatos por evento;
- validación estructural y compilación de todas las celdas del notebook.

El módulo forma parte de la versión consolidada incorporada a `main` en `5900fa5a7d982e408259760617fde1f613426f79`.

---

# 8. Módulo de Daniela — RF13, RF14 y RF16

## Estado

**✅ VALIDADO**

## Objetivo

Adaptar la salida auditada de Walter, organizar cada captura exactamente una vez y generar el reporte final sin reabrir el video ni reconstruir eventos.

### Contribución consolidada

- **Aporte:** Daniela aportó categorías, organización por temas, ReportLab y el lenguaje visual completo del PDF.
- **Qué funcionó:** el mapping de eventos, la estructura temática, la portada, las tarjetas y la diferenciación visual de categorías.
- **Desafío de integración:** la propuesta original incluía segundos y rutas reconstruidos manualmente y más de una representación de temas y renderer.
- **Adaptación necesaria:** RF13 consume rutas persistidas de Walter, RF14 conserva una única secuencia ordenada y RF16 recibe un destino explícito.
- **Resultado final:** el PDF usa el diseño visual original de Daniela sobre los datos reales de RF13/RF14 y se valida antes de su descarga.

La recuperación se implementó sobre `integration/auditoria-pizarra-snap`. La rama original de Daniela se utilizó únicamente como referencia; no se hizo merge ni cherry-pick.

## Recuperación semántica

Se recuperaron:

- el mapping visual `CAPTURA_NORMAL → NORMAL`, `CONCEPTO_IMPORTANTE → IMPORTANTE` y `FIN_DE_TEMA → FIN_DE_TEMA`;
- la organización lineal por temas;
- ReportLab, la portada, la jerarquía de tarjetas y la diferenciación visual de categorías;
- la conservación de relación de aspecto y los renglones opcionales para notas.

Se adaptaron:

- RF13 para consumir directamente `resultados_walter` y producir registros livianos;
- la selección de imagen, priorizando una procesada válida y usando la original como fallback;
- RF14 para preservar el orden global en una única lista `capturas` por tema;
- RF16 para recibir un path de salida explícito, dibujar fondos en canvas, validar el PDF y devolver un `Path`.

Se descartaron:

- `capturar_frame_completo` y los segundos hardcodeados;
- la recreación manual de eventos y rutas;
- la estructura separada `normales` / `importante` / `fin_de_tema`;
- la definición duplicada y obsoleta de `generar_pdf_clase`;
- la dependencia de `files.download`, fondos PNG relativos y outputs antiguos.

## Arquitectura implementada

```text
resultados_walter
        ↓
adaptar_para_reporte()
        ↓
resultados_reporte
        ↓
agrupar_por_temas()
        ↓
temas
        ↓
generar_pdf_clase()
        ↓
Path del PDF validado
```

---

## RF13 — Clasificación de captura

### Contrato y comportamiento

`adaptar_para_reporte(resultados_walter)` conserva identidad, evento y momento, deriva una categoría y selecciona una ruta persistida. No copia `mejor_frame`, `captura_procesada` ni las evaluaciones completas.

```python
{
    "numero_captura": int,
    "tipo_evento": str,
    "categoria": str,
    "momento_del_evento": float,
    "imagen_path": str | None,
    "fuente_imagen": "procesada" | "original" | "sin_imagen",
}
```

La selección de imagen usa este orden:

```text
captura_procesada_path válida
        ↓
captura_path válida
        ↓
None + advertencia
```

Un evento desconocido produce `ValueError`; nunca se pierde silenciosamente.

---

## RF14 — Organización por temas

### Estructura final

```python
[
    {
        "numero_tema": 1,
        "capturas": [...],
        "cerrado": True,
    },
]
```

`agrupar_por_temas(resultados_reporte)` preserva el orden de entrada y no muta la lista recibida. Cada `FIN_DE_TEMA` se incluye como última captura de su tema, marca `cerrado=True` y hace que el siguiente evento inicie un tema nuevo. Un último tema sin cierre se conserva con `cerrado=False`.

La función rechaza identificadores duplicados, eventos desconocidos y categorías incoherentes. Además valida que la cantidad total de capturas de salida coincida con la entrada.

---

## RF16 — Generación del reporte PDF

### Implementación

`generar_pdf_clase(temas, salida_pdf, datos_clase=None)` utiliza ReportLab y Pillow. La función:

- recibe un destino explícito y crea su directorio padre;
- restaura la identidad visual original diseñada por Daniela: fondos suaves, cintas de marca, logo, wordmark, portada, encabezado, pie y tarjetas A4;
- conserva la paleta teal/ámbar, los bordes por categoría y los renglones de notas de NORMAL e IMPORTANTE;
- mantiene relación de aspecto con límites de ancho y alto;
- muestra un placeholder si falta la imagen o el archivo no puede abrirse;
- genera los fondos de Daniela en un directorio temporal, sin archivos auxiliares persistentes;
- verifica existencia y tamaño del PDF;
- devuelve un `Path` absoluto;
- no depende de Colab ni llama a `files.download`.

La portada conserva los datos originales de Daniela, con las dos actualizaciones acordadas: institución `UTN` y materia `DIPLOMATURA EN IA`. `datos_clase` permite reemplazar explícitamente esos valores cuando corresponda.

### Pruebas realizadas

- RF13: mapping, identidad, tiempo, selección procesada, fallback original, ausencia de imagen, serialización y rechazo de eventos desconocidos.
- RF14: lista vacía, secuencia nominal, último tema abierto, primer cierre, cierres consecutivos, cierre final, orden, unicidad, ausencia de pérdida y no mutación.
- RF16: imágenes controladas, path procesado, fallback, archivo corrupto, placeholder, tema abierto, existencia, tamaño, apertura con `PdfReader` y páginas.
- Comparación visual renderizada contra el RF16 original de Daniela: páginas internas idénticas y portada modificada únicamente en institución y materia.

### Validación end-to-end consolidada

La prueba real se ejecutó desde un proceso limpio sobre `integration/auditoria-pizarra-snap`, utilizando el video oficial fuera del repositorio. El resultado verificado fue:

```text
CAPTURA_NORMAL       21,876 s   57 candidatos
CONCEPTO_IMPORTANTE  37,512 s   57 candidatos
FIN_DE_TEMA          50,548 s   57 candidatos
```

La etapa de selección produjo tres capturas originales válidas. RF13 generó tres `resultados_reporte`, RF14 conservó las tres capturas en un único tema cerrado y RF16 generó un PDF final válido de tres páginas con el diseño original de Daniela restaurado.

### Extensión futura

Si el tiempo y el alcance del trabajo lo permiten, se podrá evaluar posteriormente:

- OCR;
- modelo de visión;
- resumen mediante IA;
- conceptos principales;
- preguntas de repaso.

Estas funciones son complementarias y no deben impedir completar primero el flujo principal.

### Resultado final

Archivo PDF final organizado y legible.

---

# 9. Contratos y flujo entre integrantes

```text
Nicolás
RF01 → RF02 → RF03 → RF04 → RF05
 ✅      ✅      ✅      ✅      ✅
                         │
                         ▼
Diego
RF06 → RF07 → RF08 → RF09
                         │
                         ▼
Walter
RF10 → RF11 → RF12 → RF15
                         │
                         ▼
Daniela
RF13 → RF14 → RF16
```

En el flujo consolidado, cada etapa utiliza como entrada la salida validada de la etapa anterior.

### Contratos consolidados

| Frontera | Entrada recibida | Transformación | Entrega |
|---|---|---|---|
| Nicolás → Diego | Coordenadas, histogramas y estado `LIBRE/CUBIERTA` | Asociación de ROI, validación temporal y evento | `capturas` con tipo, momento y candidatos |
| Diego → Walter | `frames_candidatos` posteriores al evento | Métricas, selección, guardado y CLAHE opcional | `resultados_walter` con ganador, métricas y rutas |
| Walter → Daniela | Identidad del evento y rutas persistidas | Categoría y contrato liviano | `resultados_reporte` |
| RF13 → RF14 | Registros clasificados y ordenados | Agrupación y cierre | `temas` |
| RF14 → RF16 | Temas y capturas | Validación y composición visual | `Path` del PDF |

Estos contratos evitan que cada etapa vuelva a abrir el video o reconstruya datos que ya fueron resueltos por el módulo anterior.

### Secuencia funcional completa

```text
VIDEO Y ROI
   ↓
HISTOGRAMAS Y CAMBIOS
   ↓
COMANDO Y VALIDACIÓN
   ↓
CAPTURA POSTERIOR
   ↓
CALIDAD Y PROCESAMIENTO
   ↓
ORGANIZACIÓN Y PDF
```

### Autoría Git y responsabilidad funcional

La autoría de un commit indica quién creó ese objeto Git. La responsabilidad funcional documenta quién desarrolló el módulo original y qué aporte se preservó.

Los commits de recuperación:

```text
f7899f8 feat(rf10-rf15): recover Walter frame selection pipeline
03edc9c feat(rf13-rf16): recover Daniela reporting pipeline
```

tienen autor Git `nicodf91` porque reconstruyen semánticamente los aportes sobre la historia consolidada. Esto no traslada a Nicolás la responsabilidad funcional de RF10–RF16:

```text
Walter  — RF10–RF12 y RF15
Daniela — RF13–RF14 y RF16
```

Preservamos las ramas originales `seleccionFrame` y `feature/rf13-rf14-rf16-daniela` como evidencia de los aportes. El catálogo y la planificación de Daniela se incorporan por archivo, desde `docs/documentacion-proyecto`, con referencia a su [commit original `96ce561`](https://github.com/nicodf91/pizarra-snap/commit/96ce561c5350a9b9620eb133b42c433e81ed10b3).

---

# 10. Revisión cruzada

La tabla conserva el reparto de revisiones propuesto durante el desarrollo original.

| Responsable | Revisor sugerido |
|---|---|
| Nicolás | Diego |
| Diego | Walter |
| Walter | Daniela |
| Daniela | Nicolás |

La revisión no significa volver a desarrollar el módulo. Consiste en:

- ejecutar las celdas;
- comprobar que funcionan;
- leer los comentarios;
- confirmar que la salida coincide con lo esperado;
- informar errores antes de integrar.

---

# 11. Organización actual del repositorio

| Archivo | Uso |
|---|---|
| [README.md](README.md) | Presentación, instalación y uso del MVP |
| [PLAN_TRABAJO_PIZARRA_SNAP.md](PLAN_TRABAJO_PIZARRA_SNAP.md) | Estado técnico, decisiones e historia de integración |
| [app.py](app.py) | Carga del MP4, generación y descarga del reporte en Streamlit |
| [pipeline.py](pipeline.py) | Ejecución de RF01–RF16 fuera de Colab |
| [requirements.txt](requirements.txt) | Dependencias fijadas del entorno local |
| [notebooks/PizarraSnap.ipynb](notebooks/PizarraSnap.ipynb) | Implementación original de referencia |
| [notebooks/README.md](notebooks/README.md) | Manual para ejecutar el notebook en Google Colab |
| [docs/REQUERIMIENTOS.md](docs/REQUERIMIENTOS.md) y [docs/GANTT.md](docs/GANTT.md) | Catálogo y planificación original de Daniela, con notas de alcance del MVP |

---

# 12. Video de prueba

## Archivo utilizado

```text
proyecto_pizzarasnap.mp4
```

El video se mantiene fuera de Git normal por su tamaño y se comparte mediante Google Drive:

[Ver o descargar video de prueba](https://drive.google.com/file/d/1Vcixn88RZXEH3cLLovZQJBfYXKoIKlMb/view?usp=drive_link)

El nombre esperado durante el desarrollo es:

```text
proyecto_pizzarasnap.mp4
```

El archivo `.gitignore` excluye específicamente `/proyecto_pizzarasnap.mp4`. Otros archivos MP4 no quedan ocultos por una regla global y pueden versionarse deliberadamente si el equipo lo decide.

---

# 13. Historia y criterio de trabajo con GitHub

Durante el desarrollo se utilizó un flujo por ramas para reducir conflictos sobre el notebook oficial. El criterio sigue siendo válido para futuras contribuciones:

1. trabajar siempre desde la versión actualizada de `main`;
2. crear una rama para cada bloque de requerimientos;
3. modificar solamente el bloque correspondiente;
4. ejecutar todas las celdas necesarias antes de entregar;
5. actualizar este archivo cuando corresponda;
6. realizar commits claros;
7. abrir un Pull Request;
8. realizar la revisión cruzada;
9. integrar a `main` solamente cuando el módulo funcione.

## Ramas preservadas

| Rama | Función histórica |
|---|---|
| `feature/rf06-rf09-diego` | Implementación de Diego incorporada a la línea consolidada |
| `seleccionFrame` | Aporte original de Walter auditado semánticamente |
| `feature/rf13-rf14-rf16-daniela` | Aporte original de Daniela |
| `recovery/walter-rf10-rf12-rf15` | Recuperación compatible con el contrato de Diego |
| `recovery/daniela-rf13-rf14-rf16` | Recuperación compatible con `resultados_walter` |
| `hardening/pre-main-consolidation` | Validaciones y robustez previas a `main` |
| `fix/rf16-restaurar-estilo-daniela` | Restauración del diseño visual original |
| `docs/recuperar-identidad-equipo` | Recuperación de explicaciones compatibles |
| `docs/finalizar-estado-pre-main` | Cierre documental anterior a la promoción |
| `integration/auditoria-pizarra-snap` | Rama acumulativa validada antes del fast-forward final |

Estas ramas son evidencia histórica. Su limpieza, si alguna vez se decide, debe tratarse como una tarea independiente.

## Ejemplos de commits

```text
feat: agrega histogramas de las ROI
feat: implementa detección de cambios
feat: valida comandos visuales
feat: implementa ventana posterior al evento
feat: selecciona el mejor frame
feat: genera reporte PDF
fix: ajusta umbral del detector
docs: actualiza estado de RF04 y RF05
```

---

# 14. Regla importante para el notebook

El código se mantiene:

- simple;
- breve;
- comentado;
- didáctico;
- reproducible.

Los comentarios se escribirán como notas propias del desarrollo.

Ejemplo correcto:

```python
# Convierto la ROI a escala de grises para simplificar el análisis.
roi_gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
```

Evitar comentarios conversacionales como:

```python
# Ahora te voy a mostrar cómo convertir la imagen.
```

---

# 15. Checklist de consolidación completado

Antes de incorporar el notebook a `main`, completamos estos controles.

- [x] El código ejecutó sin errores mediante Run All con el video oficial.
- [x] Las entradas y salidas de los módulos quedaron documentadas.
- [x] RF01–RF16 incluyen comprobaciones o validaciones acordes a su alcance.
- [x] Se revisaron los resultados visuales de las capturas y del PDF.
- [x] El notebook fue validado manualmente desde una descarga de `main`.
- [x] El plan y el README registraron el estado consolidado.
- [x] Se preservaron los aportes y la responsabilidad funcional del equipo.
- [x] La historia acumulativa se verificó como fast-forward posible.
- [x] La versión consolidada se incorporó a `main` mediante fast-forward.

Para cambios futuros deben repetirse controles proporcionales al alcance. Un cambio documental no requiere reejecutar el notebook si su hash permanece idéntico; un cambio funcional sí exige una nueva validación completa.

---

# 16. Estado técnico consolidado

Validamos el MVP con Python 3.12.14 y Streamlit 1.67.0. Con el video oficial obtuvimos estos resultados.

| Resultado | Observación |
|---|---|
| Comandos en orden | `CAPTURA_NORMAL` → `CONCEPTO_IMPORTANTE` → `FIN_DE_TEMA` |
| Frames candidatos | 57 por evento |
| Capturas seleccionadas | 3 |
| Temas | 1 tema cerrado |
| Reporte | PDF legible de 3 páginas con el diseño original de Daniela |

- **Paridad del pipeline.** Comparamos el módulo con las celdas originales usando el mismo MP4. Coincidieron los eventos, los tiempos, los candidatos, los índices ganadores, las métricas, los PNG y el tema. Las tres páginas coincidieron píxel por píxel al renderizarlas con Poppler a 90 dpi. Poppler emitió los mismos avisos de fuentes en ambos PDF.
- **Interfaz.** En Chromium cargamos el video oficial, vimos el indicador de procesamiento y descargamos dos veces un PDF idéntico. Probamos también un MP4 vacío y uno ilegible con el mismo nombre que el oficial.
- **Estado y errores.** Streamlit AppTest verificó la corrida oficial y que una nueva ejecución de la interfaz conserva la descarga sin reprocesar. Al reemplazar el MP4, se elimina el resultado anterior. Los archivos vacíos o ilegibles muestran un error.
- **Entorno y pruebas de módulos.** Pasó `pip check`. Ejecutamos los casos sintéticos originales de selección, clasificación, temas y generación del reporte sobre el módulo extraído. También verificamos el caso sin eventos y la limpieza ante un fallo al generar el PDF.

La [corrida de referencia en Colab](notebooks/README.md#11-resultado-de-la-corrida-oficial-validada) sigue documentada por separado. Los resultados corresponden al MP4 oficial.

---

# 17. Historia de integración

## 10/08/2026 — Desarrollo inicial

### Nicolás

- ✅ RF01 completado.
- ✅ RF02 completado.
- ✅ RF03 completado.
- ✅ Video leído correctamente.
- ✅ Primer frame analizado como matriz NumPy.
- ✅ Píxel BGR analizado.
- ✅ Tres ROI definidas.
- ✅ Tres ROI recortadas y visualizadas.
- ✅ Base preparada para RF04.

## 10/08/2026 — Reorganización del equipo

- ✅ Equipo de trabajo reorganizado en cuatro integrantes activos.
- ✅ RF04–RF05 asignados a Nicolás.
- ✅ RF06–RF09 agrupados y asignados a Diego.
- ✅ RF10–RF12 y RF15 continúan asignados a Walter.
- ✅ RF13–RF14 y RF16 continúan asignados a Daniela.
- ✅ Flujo de dependencias actualizado.
- ✅ Revisión cruzada actualizada.
- ✅ Nombres de ramas de trabajo actualizados.
- ✅ Enlace real del video de Drive incorporado al plan.
- ✅ Próximo responsable actualizado.

### Continuidad prevista en ese momento

- Nicolás inicia RF04 y RF05.

## 11/08/2026 — RF04 y RF05 completados

### Nicolás

- ✅ ROI convertidas a escala de grises.
- ✅ Gaussian Blur aplicado con kernel `5 × 5`.
- ✅ Histogramas calculados y normalizados con norma L1.
- ✅ Comparación mediante distancia de Bhattacharyya.
- ✅ Pruebas libre vs. libre realizadas.
- ✅ Pruebas de transición realizadas.
- ✅ Coberturas claras validadas en las tres ROI.
- ✅ Movimiento cercano probado sin activación incorrecta.
- ✅ Umbral experimental `0.40` establecido.
- ✅ Funciones reutilizables para medir y clasificar estados creadas.
- ✅ Prueba automática final con `assert` superada.
- ✅ Notebook preparado en versión limpia para GitHub.
- ✅ README actualizado.
- ✅ Plan de trabajo actualizado.
- 🔁 Módulo preparado para revisión cruzada y Pull Request antes de integrar a `main`.

### Continuidad prevista en ese momento

- Diego revisa la entrega de Nicolás y continúa con RF06–RF09 desde la salida `LIBRE / CUBIERTA`.

## 15/08/2026 — RF06 a RF09 completados

### Diego

- ✅ RF06 — Identificación del comando: detecta qué ROI cambió y la asocia
  con su evento (CAPTURA_NORMAL, CONCEPTO_IMPORTANTE, FIN_DE_TEMA).
- ✅ RF07 — Validación de la acción: exige que la ROI se cubra en soledad
  (ninguna otra ROI cubierta al mismo tiempo) y que la cobertura dure
  entre 0.5s y 4s, para descartar el ruido de que el profesor pase cerca
  de la pizarra mientras escribe.
- ✅ RF08 — Ventana temporal posterior: se abre apenas se confirma el
  evento, con duración calculada en frames a partir del fps real del
  video (no se asume 30 fps fijo).
- ✅ RF09 — Captura posterior al evento: se recolectan los frames de esa
  ventana y se entregan agrupados en `capturas` (`tipo_evento`,
  `momento_del_evento`, `frames_candidatos`).
- ✅ Prueba de aceptación con `assert` superada: se detectan los 3
  comandos reales del video (~21s, ~36s, ~49s), sin falsos positivos,
  cada ventana con la cantidad esperada de frames.
- 🔁 Módulo preparado para revisión cruzada (Walter) y Pull Request antes
  de integrar a `main`.

### Continuidad prevista en ese momento

- Walter revisa la entrega de Diego y continúa con RF10–RF12 y RF15 a
  partir de `capturas`.

## 19/08/2026 — Recuperación de RF10, RF11, RF12 y RF15

### Walter

- ✅ Trabajo previo auditado semánticamente sin merge, rebase ni cherry-pick.
- ✅ RF10 adaptado a los `frames_candidatos` reales de Diego.
- ✅ RF11 selecciona un ganador explicable por evento.
- ✅ RF12 guarda la original con nombre ordenado y ruta persistente.
- ✅ RF15 conserva una mejora CLAHE solamente cuando supera criterios medibles.
- ✅ Pruebas sintéticas, filesystem, validez del notebook y recorrido real ejecutados.
- ✅ Regresión real RF06–RF09: tres eventos en orden y 57 candidatos por evento.
- ✅ Ganadores reales inspeccionados visualmente sin mano/borrador.
- ✅ Recovery auditada e incorporada a la versión consolidada validada en esa etapa.

### Daniela

- ✅ RF13 consume directamente los tres resultados de Walter.
- ✅ RF14 conserva orden, unicidad y cierre de tema.
- ⚪ Durante una validación intermedia de RF16, una versión previa generó un PDF válido de cuatro páginas.
- ✅ Pipeline real verificado con los tres eventos y 57 candidatos por evento.
- ✅ Recovery auditada e incorporada a la versión consolidada validada en esa etapa.

## 20/08/2026 — Hardening, restauración visual y documentación

- ✅ El pipeline consolidado recibió validaciones adicionales de contratos, filesystem y PDF.
- ✅ Se restauró la identidad visual original de Daniela sobre el contrato final de RF13/RF14.
- ✅ Los fondos se generan en un directorio temporal y no agregan assets al repositorio.
- ✅ La portada se actualizó únicamente con institución `UTN` y materia `DIPLOMATURA EN IA`.
- ✅ Se recuperaron comentarios y Markdown compatibles del equipo sin modificar la lógica validada.
- ✅ Se neutralizó la documentación de estado para preparar su promoción.

## 20/08/2026 — Promoción definitiva a `main`

- ✅ La rama de integración se verificó como descendiente lineal de `main`.
- ✅ Los ocho commits consolidados conservaron sus SHAs originales.
- ✅ `main` avanzó mediante fast-forward hasta `5900fa5a7d982e408259760617fde1f613426f79`.
- ✅ No se creó merge commit ni se reescribió historia.
- ✅ El notebook mantuvo el hash `583c2db6bb67f59db5d6df5155a1686ce12ee221`.

## Validación manual final desde `main`

Después de la promoción, el notebook se descargó desde GitHub, se cargó en Google Colab y se ejecutó mediante Run All con el video oficial. Generó tres capturas, un tema cerrado y un PDF final de tres páginas con descarga automática.

La diferencia entre cuatro y tres páginas refleja dos momentos de validación, no una contradicción funcional:

```text
validación intermedia → PDF de 4 páginas
restauración y renderer consolidado → PDF final de 3 páginas en la corrida oficial
```

El número de páginas depende de las capturas, los temas y la maquetación.

## 10/11/2026 — Integración de Streamlit

Incorporamos `app.py`, `pipeline.py` y `requirements.txt` mediante el [PR #5](https://github.com/nicodf91/pizarra-snap/pull/5). El notebook conservó el mismo hash. La [validación del MVP](#16-estado-técnico-consolidado) registra la paridad con el flujo original y las pruebas de la interfaz local.

---

# 18. Criterio para actualizar este documento

Cada cambio futuro debe actualizar primero el estado actual y, cuando aporte trazabilidad, agregar una entrada breve a la historia.

Ejemplo:

```markdown
## DD/MM/AAAA

### Nicolás

- ✅ Conversión de ROI a escala de grises.
- ✅ Gaussian Blur con kernel 5x5.
- ✅ Histogramas calculados.
- 🟡 Calibración del umbral en progreso.
```

De esta forma el archivo funciona simultáneamente como:

- planificación;
- reparto de responsabilidades;
- registro de avances;
- documentación de integración.

La historia debe explicar decisiones y aprendizajes. No debe convertirse en una repetición indefinida del estado actual.

---

# 19. Limitaciones vigentes

Una limitación describe el alcance dentro del cual el sistema fue validado. No implica que exista un error en la corrida oficial.

| Área | Clasificación | Descripción | Impacto actual |
|---|---|---|---|
| RF03 | LIMITACIÓN | Las ROI usan coordenadas fijas ajustadas a 1920 × 1080 y a la cámara del video oficial | Ninguno dentro del escenario validado |
| RF05 | LIMITACIÓN | El umbral `0.40` depende de cámara, iluminación, pizarra y posición de las ROI | Puede requerir calibración con otro escenario |
| Inicio | DECISIÓN DE DISEÑO | Las referencias libres se calculan alrededor del segundo `0.5` | Requiere que las tres ROI comiencen libres |
| RF09 | LIMITACIÓN | Se conservan frames completos durante las ventanas posteriores | El consumo crece con resolución, FPS y eventos |
| RF10 | DECISIÓN DE DISEÑO | El score relativo pondera 55% nitidez, 30% estabilidad y 15% contraste | Funciona para la validación actual; no es un modelo universal |
| RF13 | MEJORA FUTURA | El fallback prioriza una ruta procesada existente y luego la original | Existe margen de robustez adicional ante un archivo existente pero corrupto |
| Entrada | LIMITACIÓN | El MVP procesa MP4 pregrabados que OpenCV puede abrir | El códec, los FPS y la lectura de los frames afectan el procesamiento |
| Colab | DECISIÓN DE DISEÑO | El notebook usa `google.colab` para cargar el video y descargar el PDF | La aplicación local tiene su propia interfaz de carga y descarga |

No se detectó un bug bloqueante en el flujo validado.

---

# 20. Deuda técnica y mejoras futuras

| Tema | Estado actual | Trabajo pendiente |
|---|---|---|
| Envío por email | El MVP genera el PDF y ofrece su descarga | Diseñar e implementar el envío opcional |
| Memoria de RF09 | Los 171 candidatos de la corrida oficial suman cerca de 1 GiB sin contar las demás etapas | Medir el pico con más videos y evaluar cómo reducirlo preservando la selección |
| Otros videos | El encuadre, las ROI y el umbral se probaron con el video oficial | Ampliar la validación con otras resoluciones, FPS e iluminación antes de ajustar la calibración |
| Dependencias | La app local tiene versiones fijadas en [requirements.txt](requirements.txt). Colab instala algunas bibliotecas sin versiones | Evaluar la reproducibilidad del entorno alternativo |
| Notebook y pruebas | El notebook conserva sus salidas y casos sintéticos. Verificamos el MVP por fuera del notebook | Revisar la automatización de pruebas y, en una tarea aparte, el tamaño de las salidas guardadas |
| Robustez de RF13 | Una ruta existente pero ilegible puede terminar en un marcador de imagen no disponible | Evaluar el fallback al PNG original cuando la versión procesada esté dañada |

OCR, resúmenes y cámara en vivo quedan fuera del alcance validado.

---

# 21. Glosario

| Término | Explicación dentro de Pizarra Snap |
|---|---|
| Frame | Imagen individual del video que todavía se encuentra en memoria |
| ROI | Región de interés: recorte rectangular observado como comando visual |
| Histograma | Resumen de cuántos píxeles existen en cada intensidad de gris |
| Umbral | Valor que separa los estados técnicos `LIBRE` y `CUBIERTA` |
| FPS | Frames por segundo informados por el video |
| Evento | Acción validada después de completar `LIBRE → CUBIERTA → LIBRE` |
| `tipo_evento` | Identificador técnico: `CAPTURA_NORMAL`, `CONCEPTO_IMPORTANTE` o `FIN_DE_TEMA` |
| Categoría | Clasificación usada por el reporte: `NORMAL`, `IMPORTANTE` o `FIN_DE_TEMA` |
| Ventana temporal | Intervalo posterior al evento durante el cual se recolectan imágenes |
| Frame candidato | Una de las imágenes conservadas para comparar su calidad |
| Captura | Frame ganador o registro persistido después de la selección |
| Captura original | Frame ganador guardado sin reemplazar su contenido |
| Captura procesada | Versión gris con CLAHE conservada sólo si supera criterios de calidad |
| Laplaciano | Operador utilizado para estimar nitidez mediante la varianza de sus respuestas |
| Contraste | Dispersión de intensidades medida mediante desviación estándar |
| CLAHE | Mejora local de contraste con límite para evitar amplificación excesiva |
| Pipeline | Cadena completa de etapas conectadas desde el video hasta el PDF |
| Contrato | Estructura de datos acordada entre dos módulos |
| Tema | Grupo ordenado de capturas, cerrado opcionalmente por `FIN_DE_TEMA` |
| ReportLab | Biblioteca que construye y maqueta el PDF |
| Fast-forward | Avance de una rama hasta un descendiente sin crear un merge commit |

Convenciones de lenguaje:

```text
frame     → imagen todavía en memoria
captura   → ganador o registro persistido
evento    → acción detectada y validada
categoría → clasificación utilizada por el reporte
LIBRE / CUBIERTA → estados técnicos de una ROI
```

La documentación utiliza “pizarra” de forma consistente y denomina **Run All** a la ejecución completa del notebook.

---

# 22. Próximos pasos

El [registro de mejoras](#20-deuda-técnica-y-mejoras-futuras) reúne el trabajo pendiente. Al incorporar cambios funcionales, repetiremos la prueba con el MP4 oficial para comprobar que se conservan los resultados de RF01–RF16.
