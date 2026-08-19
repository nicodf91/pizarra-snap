# Pizarra Snap — Plan de trabajo colaborativo

**Proyecto:** Pizarra Snap  
**Equipo actual:** Nicolás, Diego, Walter y Daniela  
**Documento vivo:** este archivo debe actualizarse a medida que cada módulo se complete, pruebe e integre.  
**Última actualización:** 19/08/2026

---

## 1. Objetivo del proyecto

Pizarra Snap es un sistema de visión por computadora pensado para asistir a docentes durante una clase presencial.

Una cámara fija observa la pizarra. El docente puede generar tres tipos de eventos cubriendo brevemente una zona visual con un elemento cotidiano, como el borrador:

- 📸 **CAPTURA NORMAL**
- ⭐ **CONCEPTO IMPORTANTE**
- 📌 **FIN DE TEMA**

El sistema detectará visualmente el evento, esperará a que la zona vuelva a quedar visible y analizará una breve secuencia de frames **posteriores** a la acción para seleccionar la mejor imagen. Las capturas se clasificarán y posteriormente se utilizarán para generar un reporte PDF organizado por temas.

> La arquitectura vigente trabaja con frames **posteriores al evento**. No se utiliza un buffer retrospectivo como parte del flujo principal.

---

## 2. Criterio general de trabajo

El proyecto se divide siguiendo los requerimientos funcionales RF01–RF16.

Cada módulo deberá:

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
| ✅ REALIZADO | Código implementado y validado por el responsable |
| 🟡 EN PROGRESO | El integrante está trabajando en el módulo |
| ⬜ PENDIENTE | Todavía no comenzó |
| 🔁 EN REVISIÓN | Implementado y pendiente de revisión cruzada antes de integrar |
| ⚠️ AJUSTE | Funciona, pero requiere calibración o mejora |

---

# 4. Estado general del proyecto

| RF | Requerimiento | Responsable | Estado |
|---|---|---|---|
| RF01 | Lectura de video | Nicolás | ✅ REALIZADO |
| RF02 | Procesamiento de frames | Nicolás | ✅ REALIZADO |
| RF03 | Regiones de interés (ROI) | Nicolás | ✅ REALIZADO |
| RF04 | Análisis de histogramas | Nicolás | ✅ REALIZADO |
| RF05 | Detección de cambios | Nicolás | ✅ REALIZADO |
| RF06 | Identificación del comando | Diego | ✅ REALIZADO |
| RF07 | Validación de la acción | Diego | ✅ REALIZADO |
| RF08 | Ventana temporal posterior | Diego | ✅ REALIZADO |
| RF09 | Captura posterior al evento | Diego | ✅ REALIZADO |
| RF10 | Evaluación de calidad | Walter | 🔁 EN REVISIÓN |
| RF11 | Selección del mejor frame | Walter | 🔁 EN REVISIÓN |
| RF12 | Guardado de captura | Walter | 🔁 EN REVISIÓN |
| RF13 | Clasificación de captura | Daniela | ⬜ PENDIENTE |
| RF14 | Organización por temas | Daniela | ⬜ PENDIENTE |
| RF15 | Procesamiento de imagen | Walter | 🔁 EN REVISIÓN |
| RF16 | Generación de reporte PDF | Daniela | ⬜ PENDIENTE |

---

# 5. Módulo de Nicolás — RF01 a RF05

## Estado

```text
RF01 ✅ REALIZADO
RF02 ✅ REALIZADO
RF03 ✅ REALIZADO
RF04 ✅ REALIZADO
RF05 ✅ REALIZADO
```

## Objetivo general del módulo

Construir la base de visión por computadora del proyecto: leer el video, trabajar con sus frames, definir las tres ROI y transformar esas regiones en señales capaces de indicar si una zona está libre o cubierta.

---

## RF01 — Lectura de video

### Trabajo realizado

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
RF06 ✅ REALIZADO
RF07 ✅ REALIZADO
RF08 ✅ REALIZADO
RF09 ✅ REALIZADO
```

## Objetivo general del módulo

Convertir los cambios de las ROI en comandos reales, validar que la acción sea intencional y, después del evento confirmado, abrir una ventana temporal para recolectar los frames candidatos.

Esta agrupación mantiene juntas dos etapas fuertemente relacionadas:

```text
DETECTAR COMANDO → VALIDAR EVENTO → ABRIR VENTANA → RECOLECTAR FRAMES
```

---

## RF06 — Identificación del comando

### Tareas previstas

Relacionar cada ROI con su evento:

```text
ROI Captura normal      → CAPTURA_NORMAL
ROI Concepto importante → CONCEPTO_IMPORTANTE
ROI Fin de tema         → FIN_DE_TEMA
```

- Detectar qué zona fue activada.
- Evitar confundir una ROI con otra.
- Guardar el tipo de evento en una variable clara.

### Resultado esperado

Generar uno de estos eventos:

```text
CAPTURA_NORMAL
CONCEPTO_IMPORTANTE
FIN_DE_TEMA
```

---

## RF07 — Validación de la acción

### Tareas previstas

Implementar la secuencia válida:

```text
VISIBLE → CUBIERTA → VISIBLE
```

La acción no debe validarse mientras el símbolo continúe tapado.

Se deberá considerar:

- duración mínima de la cobertura;
- retorno de la ROI al estado visible;
- bloqueo temporal para evitar duplicados;
- falsos positivos.

### Resultado esperado

Evento único y validado solamente después de que la zona vuelva a quedar visible.

Variables esperadas o equivalentes:

```text
evento_validado
tipo_evento
momento_del_evento
```

---

## RF08 — Ventana temporal posterior

### Tareas previstas

- Comenzar la ventana únicamente después de RF07.
- Trabajar con una duración inicial aproximada de **2 segundos**.
- Calcular cuántos frames corresponden a esa ventana utilizando los FPS reales.
- Tener en cuenta que el video de prueba presenta FPS no entero.
- Evitar depender innecesariamente de un valor fijo de 30 FPS.
- Almacenar solamente los frames candidatos de esa ventana.

### Resultado esperado

Lista o colección de frames obtenidos después de la activación.

---

## RF09 — Captura posterior al evento

### Tareas previstas

- Leer los frames durante la ventana.
- Numerarlos o asociarlos con su posición temporal.
- Guardarlos temporalmente como candidatos.
- Finalizar correctamente la ventana.
- No conservar indefinidamente frames que ya no sean necesarios.

### Resultado esperado

Conjunto de frames candidatos listo para evaluar la calidad.

### Entrega de Diego a Walter

Diego deberá entregar una estructura semejante a:

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

Cada `frames_candidatos` guarda frames completos en memoria (resolución
completa, sin comprimir) — con 3 capturas de ~57 frames cada una esto ya
ocupa varios cientos de MB de RAM. Si el video de prueba real fuera más
largo o hubiera más eventos, convendría revisar esto (por ejemplo,
guardar menos frames por ventana o reducir resolución) antes de RF10.

---

# 7. Módulo de Walter — RF10, RF11, RF12 y RF15

## Estado

**🔁 EN REVISIÓN**

## Objetivo

Elegir automáticamente la mejor captura posterior al evento, guardarla y mejorar la imagen de la pizarra cuando una transformación aporte valor real.

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

En Colab se usa `/content/capturas_pizarra_snap`; en ejecución local, el directorio temporal del sistema. Así las imágenes generadas no contaminan el repositorio.

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

El módulo queda en revisión hasta la auditoría cruzada de la rama de recuperación.

---

# 8. Módulo de Daniela — RF13, RF14 y RF16

## Estado

**⬜ PENDIENTE**

## Objetivo

Organizar las capturas según el significado del evento y generar el reporte final.

---

## RF13 — Clasificación de captura

### Tareas previstas

Clasificar cada captura como:

```text
NORMAL
IMPORTANTE
FIN_DE_TEMA
```

Mantener una estructura ordenada con los datos necesarios.

---

## RF14 — Organización por temas

### Tareas previstas

- Mantener un tema activo.
- Agregar capturas normales al tema correspondiente.
- Destacar las capturas IMPORTANTES.
- Cuando aparezca FIN_DE_TEMA:
  - incluir la captura final;
  - cerrar el bloque;
  - preparar un nuevo tema.

### Resultado esperado

Estructura lógica de la clase:

```text
Tema 1
├── Captura normal
├── Captura normal
├── Concepto importante
└── Fin de tema

Tema 2
├── ...
```

---

## RF16 — Generación del reporte PDF

### Tareas previstas

Generar un PDF que incluya:

- identificación de Pizarra Snap;
- fecha o datos de la clase si están disponibles;
- separación visual por temas;
- capturas normales;
- conceptos importantes destacados;
- cierre de cada tema;
- imágenes procesadas.

### Extensión futura

Si el tiempo y el alcance del trabajo lo permiten, se podrá evaluar posteriormente:

- OCR;
- modelo de visión;
- resumen mediante IA;
- conceptos principales;
- preguntas de repaso.

Estas funciones son complementarias y no deben impedir completar primero el flujo principal.

### Resultado esperado

Archivo PDF final organizado y legible.

---

# 9. Flujo de dependencias entre integrantes

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

Cada integrante debe comenzar utilizando como entrada la salida validada del módulo anterior.

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

---

# 10. Revisión cruzada

Para evitar que cada integrante trabaje de manera aislada, los módulos tendrán un responsable principal y otra persona que deberá probarlos antes de integrarlos a `main`.

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

```text
pizarra-snap/
│
├── .gitignore
├── README.md
├── PLAN_TRABAJO_PIZARRA_SNAP.md
│
└── notebooks/
    ├── README.md
    └── PizarraSnap.ipynb
```

## Archivos principales

### `README.md`

Portada del proyecto: objetivo, equipo actual, estado resumido, flujo general y enlaces importantes.

### `PLAN_TRABAJO_PIZARRA_SNAP.md`

Este documento. Contiene la planificación detallada, responsabilidades, dependencias, revisiones y registro de avances.

### `notebooks/PizarraSnap.ipynb`

Notebook oficial de desarrollo.

### `notebooks/README.md`

Explica la finalidad de la carpeta de notebooks.

> Nuevas carpetas como `data/`, `docs/` o `captures/` se crearán solamente cuando exista una necesidad concreta. No se documentarán como parte de la estructura actual antes de existir.

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

El archivo `.gitignore` evita subir archivos `.mp4` accidentalmente al repositorio.

---

# 13. Flujo de trabajo con GitHub

Para reducir conflictos sobre el notebook oficial:

1. trabajar siempre desde la versión actualizada de `main`;
2. crear una rama para cada bloque de requerimientos;
3. modificar solamente el bloque correspondiente;
4. ejecutar todas las celdas necesarias antes de entregar;
5. actualizar este archivo cuando corresponda;
6. realizar commits claros;
7. abrir un Pull Request;
8. realizar la revisión cruzada;
9. integrar a `main` solamente cuando el módulo funcione.

## Ramas sugeridas

```text
feature/rf04-rf05-nicolas
feature/rf06-rf09-diego
feature/rf10-rf12-rf15-walter
feature/rf13-rf14-rf16-daniela
```

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

El código deberá mantenerse:

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

# 15. Checklist antes de integrar un módulo a `main`

Antes de integrar un módulo:

- [ ] El código ejecuta sin errores.
- [ ] Los comentarios son claros.
- [ ] Se entiende la entrada del módulo.
- [ ] Se entiende la salida del módulo.
- [ ] Existe al menos una prueba.
- [ ] El responsable revisó los resultados.
- [ ] El notebook fue actualizado.
- [ ] `PLAN_TRABAJO_PIZARRA_SNAP.md` fue actualizado.
- [ ] El revisor cruzado pudo ejecutarlo.
- [ ] El Pull Request fue revisado.
- [ ] El cambio fue integrado a la rama principal.

---

# 16. Próximo paso del proyecto

La rama `recovery/walter-rf10-rf12-rf15` debe ser auditada en modo solo lectura antes de autorizar cualquier integración. RF13, RF14 y RF16 no forman parte de esta recuperación y no se conectarán hasta que el contrato de salida documentado en la sección 7 sea revisado.

No corresponde abrir ni mergear un Pull Request en esta etapa.

---

# 17. Historial de avances

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
- ✅ Ramas sugeridas actualizadas.
- ✅ Enlace real del video de Drive incorporado al plan.
- ✅ Próximo responsable actualizado.

### Próximo paso en ese momento

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

### Próximo paso

- Diego revisa la entrega de Nicolás y continúa con RF06–RF09 desde la salida `LIBRE / CUBIERTA`.

## 15/08/2026 — RF06 a RF09 completados

### Diego

- ✅ RF06 — Identificación del comando: detecta qué ROI cambió y la asocia
  con su evento (CAPTURA_NORMAL, CONCEPTO_IMPORTANTE, FIN_DE_TEMA).
- ✅ RF07 — Validación de la acción: exige que la ROI se cubra en soledad
  (ninguna otra ROI cubierta al mismo tiempo) y que la cobertura dure
  entre 0.5s y 4s, para descartar el ruido de que el profesor pase cerca
  del pizarrón mientras escribe.
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

### Próximo paso

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
- 🔁 Rama de recuperación preparada para auditoría externa; no integrada.

---

# 18. Regla para actualizar este documento

Cada vez que un integrante complete trabajo, agregar una entrada al historial.

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
