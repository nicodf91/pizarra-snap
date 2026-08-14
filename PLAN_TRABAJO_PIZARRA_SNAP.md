# Pizarra Snap — Plan de trabajo colaborativo

**Proyecto:** Pizarra Snap  
**Equipo actual:** Nicolás, Diego, Walter y Daniela  
**Documento vivo:** este archivo debe actualizarse a medida que cada módulo se complete, pruebe e integre.  
**Última actualización:** 14/08/2026

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
| RF06 | Identificación del comando | Diego | ⬜ PENDIENTE |
| RF07 | Validación de la acción | Diego | ⬜ PENDIENTE |
| RF08 | Ventana temporal posterior | Diego | ⬜ PENDIENTE |
| RF09 | Captura posterior al evento | Diego | ⬜ PENDIENTE |
| RF10 | Evaluación de calidad | Walter | ⬜ PENDIENTE |
| RF11 | Selección del mejor frame | Walter | ⬜ PENDIENTE |
| RF12 | Guardado de captura | Walter | ⬜ PENDIENTE |
| RF13 | Clasificación de captura | Daniela | ✅ REALIZADO |
| RF14 | Organización por temas | Daniela |  ✅ REALIZADO |
| RF15 | Procesamiento de imagen | Walter | ⬜ PENDIENTE |
| RF16 | Generación de reporte PDF | Daniela |  ✅ REALIZADO |

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

**⬜ PENDIENTE**

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

---

# 7. Módulo de Walter — RF10, RF11, RF12 y RF15

## Estado

**⬜ PENDIENTE**

## Objetivo

Elegir automáticamente la mejor captura posterior al evento, guardarla y mejorar la imagen de la pizarra cuando una transformación aporte valor real.

---

## RF10 — Evaluación de calidad

### Tareas previstas

Evaluar criterios como:

- nitidez;
- estabilidad;
- movimiento;
- contraste.

### Kernel y convolución

Utilizar el concepto de kernel donde aporte valor real.

Ejemplos previstos:

- Laplaciano para estimar nitidez;
- varianza del Laplaciano;
- comparación de movimiento entre frames.

### Resultado esperado

Asignar un puntaje de calidad a cada frame candidato.

---

## RF11 — Selección del mejor frame

### Tareas previstas

- Comparar los puntajes.
- Seleccionar automáticamente el candidato de mayor calidad.
- Verificar que el resultado no contenga innecesariamente:
  - mano;
  - borrador;
  - movimiento excesivo;
  - desenfoque.

### Resultado esperado

Un único `mejor_frame`.

---

## RF12 — Guardado de captura

### Tareas previstas

- Guardar la imagen elegida.
- Crear nombres de archivo ordenados.
- Asociarla con:
  - número de captura;
  - tipo de evento;
  - tema actual;
  - momento de captura si corresponde.

### Resultado esperado

Archivo de imagen persistente y metadatos necesarios para el módulo de organización.

---

## RF15 — Procesamiento de imagen

### Tareas previstas

Evaluar y aplicar solamente cuando aporte una mejora real:

- recorte de pizarra;
- escala de grises;
- mejora de contraste;
- reducción de ruido;
- threshold;
- Canny;
- contornos;
- corrección de perspectiva;
- operaciones morfológicas;
- erosión;
- dilatación;
- kernels `3 × 3` o `5 × 5`.

### Criterio

No se incorporarán operaciones solamente para demostrar que fueron vistas en clase. Cada transformación deberá tener una justificación relacionada con la calidad final de la pizarra.

### Entrega de Walter a Daniela

Walter deberá entregar:

- captura elegida;
- captura procesada, si corresponde;
- categoría del evento;
- metadatos necesarios para organizar el reporte.

---

# 8. Módulo de Daniela — RF13, RF14 y RF16

## Estado

```text
RF13 ✅ REALIZADO
RF14 ✅ REALIZADO
RF16 ✅ REALIZADO
```

## Objetivo

Organizar las capturas según el significado del evento y generar el reporte final.

---

## RF13 — Clasificación de captura

### Trabajo realizado

- Clasificación de eventos en NORMAL, IMPORTANTE y FIN_DE_TEMA.
- Registro de cada captura con ID, evento, categoría y momento.
- **Corrección de contrato de datos** (detectada al iniciar RF16): se agregó el campo `imagen_path` al registro, fijo en `None` hasta que exista RF12 (Walter). No se expuso como parámetro configurable, para evitar que algún módulo lo complete antes de tiempo.
- Pruebas automáticas con `assert`.
- Validación de los tres tipos de captura y del evento no reconocido.
- RF13 validado y subido a la rama `feature/rf13-rf14-rf16-daniela`.

### Contrato de datos actual

```python
{
    "id": ...,
    "evento": ...,
    "categoria": ...,
    "momento": ...,
    "tema": ...,
    "imagen_path": ...   # None hasta que RF12 exista
}
```

---

## RF14 — Organización por temas

### Trabajo realizado

- `asignar_tema(registros)`: asigna número de tema secuencial; el contador incrementa recién después de procesar un `FIN_DE_TEMA`.
- `organizar_por_temas(registros)`: agrupa en una lista de temas, cada uno con capturas normales, importante y cierre.
- Pruebas automáticas con `assert`, validando la asignación y agrupación correcta.
- RF14 validado y subido a la rama `feature/rf13-rf14-rf16-daniela`.

### Resultado obtenido

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

### Trabajo realizado

- Identidad visual V1 definida: logo (símbolo de encuadre + destello, combinado con el wordmark "Pizarra Snap"), paleta (`#FAFAFA`, `#157A6E`, `#F5A623`, `#1A1A1A`, `#6B7280`) y tipografía (Helvetica estándar de ReportLab).
- PDF generado con **ReportLab**: portada con logo protagonista, encabezado/pie con logo chico en páginas interiores, contenido organizado por tema.
- **Layout iterado tras revisión:** primera versión con grilla de 2 columnas descartada por reducir demasiado el tamaño de las imágenes. Versión final con imagen protagonista (una captura por fila, ocupando el ancho útil de la página, proporción calculada dinámicamente).
- Tratamiento visual diferencial: `NORMAL` con borde gris sutil, `IMPORTANTE` con borde ámbar, `FIN_DE_TEMA` con borde teal (cierre del bloque).
- Placeholder ("Imagen pendiente — RF12") mientras `imagen_path` sea `None`, listo para reemplazarse automáticamente cuando RF12 exista.
- Validado con capturas reales extraídas del video (frames completos en los segundos ya validados como libres por RF05) y con prueba automática (`assert`): generación sin errores, PDF válido, al menos 2 páginas, estructura de datos consistente con RF14.
- RF16 validado y subido a la rama `feature/rf13-rf14-rf16-daniela`.

### Extensión futura

Si el tiempo y el alcance del trabajo lo permiten, se podrá evaluar posteriormente:

- OCR;
- modelo de visión;
- resumen mediante IA;
- conceptos principales;
- preguntas de repaso;
- detección de diferencias entre capturas consecutivas (ver observación en sección 8bis).

Estas funciones son complementarias y no deben impedir completar primero el flujo principal.

### Resultado obtenido

Archivo PDF final organizado y legible, con identidad visual propia de Pizarra Snap.

---

# 8bis. Observación de diseño — Efecto acumulativo de las capturas

## Contexto

Al validar RF16 con imágenes reales se detectó que las capturas sucesivas de un mismo tema muestran contenido acumulado: si el docente no borra la pizarra entre una captura y la siguiente, cada imagen nueva incluye todo lo escrito anteriormente, no solo lo agregado desde la última captura.

## Por qué ocurre

No es un error de ningún RF. La cámara fotografía el estado completo de la pizarra en cada momento; ningún módulo actual (RF01-RF16) compara o resta contenido entre capturas sucesivas. Se confirmó que ni RF10-RF12 (selección del mejor frame completo) ni RF15 (recorte del marco de la pizarra respecto de su entorno) resuelven esto — ninguno aísla "solo lo nuevo" de una captura.

## Recomendación

- **Corto plazo (uso del sistema):** el docente debería borrar la pizarra al cerrar cada tema (evento FIN_DE_TEMA), antes de continuar con el siguiente.
- **Largo plazo (extensión futura):** una funcionalidad de detección de diferencias entre capturas consecutivas (similar a la comparación de histogramas ya usada en RF05, aplicada a la pizarra completa) podría aislar el contenido nuevo. Fuera del alcance del MVP actual.

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

## Próximo responsable

**Diego**

## Módulo

```text
RF06 — Identificación del comando
RF07 — Validación de la acción
RF08 — Ventana temporal posterior
RF09 — Captura posterior al evento
```

## Punto exacto desde donde continúa

El módulo de Nicolás deja disponibles:

```text
coordenadas de las tres ROI
histogramas normalizados
umbral_cobertura = 0.40
calcular_histograma_roi(...)
obtener_roi_en_segundo(...)
medir_distancia_roi(...)
clasificar_estado_roi(...)
detectar_estado_roi(...)
```

La salida principal por ROI es:

```text
(distancia, estado)
```

con `estado` igual a `LIBRE` o `CUBIERTA`.

El siguiente trabajo comienza asociando cada ROI con su comando y validando la secuencia temporal de una acción real.

### Secuencia prevista

```text
LIBRE / CUBIERTA
      ↓
IDENTIFICAR QUÉ ROI CAMBIÓ
      ↓
ASOCIAR COMANDO
      ↓
VALIDAR VISIBLE → CUBIERTA → VISIBLE
      ↓
ABRIR VENTANA POSTERIOR
      ↓
RECOLECTAR FRAMES CANDIDATOS
```

> Para la ejecución continua, Diego deberá usar referencias limpias inicializadas de forma reproducible, en lugar de depender de los segundos manuales utilizados durante la calibración experimental de RF05.

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

## 13-14/08/2026 — RF13 corregido, RF14 y RF16 completados

### Daniela

- ✅ RF13: corrección de contrato de datos — se agregó el campo `imagen_path` (fijo en `None` hasta que exista RF12).
- ✅ RF13: se corrigió la ubicación del notebook — el trabajo se había subido como archivo nuevo en la raíz del repo en vez de actualizar `notebooks/PizarraSnap.ipynb`. Consolidado en un único archivo.
- ✅ RF14: `asignar_tema` y `organizar_por_temas` implementados y validados con `assert`.
- ✅ RF16: identidad visual V1 definida (logo, paleta, tipografía).
- ✅ RF16: layout iterado — de grilla de 2 columnas a imagen protagonista en columna única, tras revisión de legibilidad.
- ✅ RF16: `generar_pdf_clase` completo, validado con capturas reales del video y prueba automática.
- 🟡 Observación de diseño detectada y documentada: efecto acumulativo de capturas cuando no se borra la pizarra entre temas (ver sección 8bis).
- ✅ Pull Request creado hacia `main`, con revisión solicitada a Nicolás.

### Próximo paso

- Nicolás revisa el módulo de Daniela (RF13/RF14/RF16), según la tabla de revisión cruzada.
- Pendiente: integración real con RF12 (Walter) para reemplazar la asignación manual de `imagen_path` por la automática.

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
