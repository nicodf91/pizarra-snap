# Pizarra Snap — Plan de trabajo colaborativo

**Proyecto:** Pizarra Snap  
**Equipo actual:** Nicolás, Diego, Walter y Daniela  
**Documento vivo:** este archivo debe actualizarse a medida que cada módulo se complete, pruebe e integre.  
**Última actualización:** 10/08/2026

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
| ✅ REALIZADO | Código implementado y validado |
| 🟡 EN PROGRESO | El integrante está trabajando en el módulo |
| ⬜ PENDIENTE | Todavía no comenzó |
| 🔁 EN REVISIÓN | Implementado y pendiente de prueba/revisión |
| ⚠️ AJUSTE | Funciona, pero requiere calibración o mejora |

---

# 4. Estado general del proyecto

| RF | Requerimiento | Responsable | Estado |
|---|---|---|---|
| RF01 | Lectura de video | Nicolás | ✅ REALIZADO |
| RF02 | Procesamiento de frames | Nicolás | ✅ REALIZADO |
| RF03 | Regiones de interés (ROI) | Nicolás | ✅ REALIZADO |
| RF04 | Análisis de histogramas | Nicolás | ⬜ PENDIENTE |
| RF05 | Detección de cambios | Nicolás | ⬜ PENDIENTE |
| RF06 | Identificación del comando | Diego | ⬜ PENDIENTE |
| RF07 | Validación de la acción | Diego | ⬜ PENDIENTE |
| RF08 | Ventana temporal posterior | Diego | ⬜ PENDIENTE |
| RF09 | Captura posterior al evento | Diego | ⬜ PENDIENTE |
| RF10 | Evaluación de calidad | Walter | ⬜ PENDIENTE |
| RF11 | Selección del mejor frame | Walter | ⬜ PENDIENTE |
| RF12 | Guardado de captura | Walter | ⬜ PENDIENTE |
| RF13 | Clasificación de captura | Daniela | ⬜ PENDIENTE |
| RF14 | Organización por temas | Daniela | ⬜ PENDIENTE |
| RF15 | Procesamiento de imagen | Walter | ⬜ PENDIENTE |
| RF16 | Generación de reporte PDF | Daniela | ⬜ PENDIENTE |

---

# 5. Módulo de Nicolás — RF01 a RF05

## Estado

```text
RF01 ✅ REALIZADO
RF02 ✅ REALIZADO
RF03 ✅ REALIZADO
RF04 ⬜ PENDIENTE
RF05 ⬜ PENDIENTE
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

Las coordenadas se consideran **válidas para continuar el proyecto**.

Durante RF04/RF05 se comprobará experimentalmente si el tamaño de alguna ROI necesita una calibración mínima para mejorar la diferencia entre histogramas. Ese eventual ajuste forma parte de la calibración del detector y no reabre RF03.

### Base disponible para RF04/RF05

- video correctamente abierto;
- frames accesibles;
- frame base validado;
- coordenadas de las tres ROI;
- variables `roi_normal`, `roi_importante` y `roi_fin`;
- notebook funcionando hasta RF03.

---

## RF04 — Análisis de histogramas

### Estado

**⬜ PENDIENTE**

### Tareas previstas

- Convertir cada ROI de BGR a escala de grises.
- Aplicar un suavizado para reducir pequeñas variaciones de iluminación.
- Utilizar `GaussianBlur`.
- Incorporar el concepto de **kernel o matriz de convolución**, inicialmente con un kernel de `5 × 5`.
- Calcular el histograma de cada ROI.
- Normalizar los histogramas si corresponde.
- Graficar y explicar los histogramas.
- Obtener ejemplos de:
  - ROI libre;
  - ROI cubierta.
- Comparar cuantitativamente ambos estados.

### Conceptos de la Diplomatura involucrados

- escala de grises;
- kernel;
- convolución;
- Gaussian Blur;
- histogramas;
- arrays NumPy;
- OpenCV;
- Matplotlib.

### Resultado esperado

Una función o procedimiento capaz de recibir una ROI y producir una representación preparada para comparar su estado visual.

---

## RF05 — Detección de cambios

### Estado

**⬜ PENDIENTE**

### Tareas previstas

- Elegir una métrica de comparación de histogramas.
- Comparar el estado de referencia con los frames siguientes.
- Experimentar con un umbral de cambio.
- Medir:
  - ROI libre contra ROI libre;
  - ROI libre contra ROI cubierta.
- Ajustar el umbral para reducir falsos positivos.
- Verificar el comportamiento frente a:
  - sombras;
  - pequeños cambios de iluminación;
  - movimiento cercano;
  - cobertura intencional del símbolo.

### Resultado esperado

Detectar de manera confiable si una ROI cambió suficientemente como para considerarla cubierta.

### Entrega de Nicolás a Diego

La salida debe permitir saber para cada ROI si se encuentra:

```text
LIBRE
o
CUBIERTA
```

Además deberán quedar disponibles las variables y/o funciones necesarias para que RF06 pueda identificar cuál de las tres zonas fue activada.

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
 ✅      ✅      ✅      ⬜      ⬜
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

Para evitar que cada integrante trabaje de manera aislada, los módulos pendientes tendrán un responsable principal y otra persona que deberá probarlos antes de considerarlos cerrados.

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

# 15. Checklist para cerrar un módulo

Antes de cambiar un módulo a **✅ REALIZADO**:

- [ ] El código ejecuta sin errores.
- [ ] Los comentarios son claros.
- [ ] Se entiende la entrada del módulo.
- [ ] Se entiende la salida del módulo.
- [ ] Existe al menos una prueba.
- [ ] El responsable revisó los resultados.
- [ ] El revisor cruzado pudo ejecutarlo.
- [ ] El notebook fue actualizado.
- [ ] `PLAN_TRABAJO_PIZARRA_SNAP.md` fue actualizado.
- [ ] El cambio fue integrado a la rama principal.

---

# 16. Próximo paso del proyecto

## Próximo responsable

**Nicolás**

## Módulo

```text
RF04 — Análisis de histogramas
RF05 — Detección de cambios
```

## Punto exacto desde donde continúa

El notebook ya dispone de:

```text
roi_normal
roi_importante
roi_fin
```

y de las coordenadas de las tres regiones.

El siguiente trabajo comienza directamente con el preprocesamiento de estas ROI y la comparación de histogramas.

### Secuencia inicial prevista

```text
ROI
 ↓
ESCALA DE GRISES
 ↓
GAUSSIAN BLUR (kernel 5x5)
 ↓
HISTOGRAMA
 ↓
COMPARACIÓN
 ↓
UMBRAL
 ↓
LIBRE / CUBIERTA
```

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

### Próximo paso

- ⬜ Nicolás inicia RF04 y RF05.

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
