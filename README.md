# 📸 Pizarra Snap

**Sistema inteligente de captura de pizarras mediante visión por computadora.**

Proyecto desarrollado como trabajo colaborativo para la **Diplomatura en Inteligencia Artificial**.

---

## 🎯 Objetivo

Pizarra Snap busca permitir que un docente capture el contenido de una pizarra sin utilizar:

- teclado;
- mouse;
- botones electrónicos;
- comandos de voz.

La interacción se realiza mediante tres zonas visuales ubicadas sobre la pizarra:

- 📸 **Captura normal**
- ⭐ **Concepto importante**
- 📌 **Fin de tema**

El docente activa una acción cubriendo brevemente la zona correspondiente.

El sistema detecta el cambio mediante técnicas de visión por computadora y, una vez que la zona vuelve a quedar visible, analiza una breve secuencia de frames posteriores para seleccionar automáticamente la imagen de mejor calidad.

---

## 🧠 Flujo general

```text
CÁMARA
   ↓
VIDEO
   ↓
FRAMES
   ↓
REGIONES DE INTERÉS (ROI)
   ↓
HISTOGRAMAS
   ↓
DETECCIÓN DEL EVENTO
   ↓
CAPTURA POSTERIOR
   ↓
EVALUACIÓN DE CALIDAD
   ↓
MEJOR FRAME
   ↓
CLASIFICACIÓN
   ↓
PROCESAMIENTO
   ↓
REPORTE PDF
```

---

## 🛠️ Stack tecnológico

El proyecto utiliza principalmente herramientas trabajadas durante la Diplomatura:

- **Python**
- **Google Colab / Jupyter Notebook**
- **OpenCV**
- **NumPy**
- **Matplotlib**

Durante las siguientes etapas se evaluará incorporar:

- ReportLab o FPDF;
- OCR;
- modelos de visión;
- modelos de lenguaje para generación de resúmenes.

---

## 👥 Equipo

El proyecto está desarrollado por:

- **Nicolás**
- **Lucas**
- **Patricia**
- **Diego**
- **Walter**
- **Daniela**

---

## 📋 Distribución del trabajo

| Integrante | Requerimientos | Responsabilidad | Estado |
|---|---|---|---|
| Nicolás | RF01–RF03 | Video, frames y regiones de interés | ✅ Realizado |
| Lucas | RF04–RF05 | Histogramas y detección de cambios | ⬜ Pendiente |
| Patricia | RF06–RF07 | Identificación y validación de comandos | ⬜ Pendiente |
| Diego | RF08–RF09 | Ventana temporal y captura posterior | ⬜ Pendiente |
| Walter | RF10–RF12 + RF15 | Calidad, mejor frame y procesamiento | ⬜ Pendiente |
| Daniela | RF13–RF14 + RF16 | Clasificación, organización y PDF | ⬜ Pendiente |

La planificación detallada y el registro de avances se encuentran en:

➡️ [PLAN_TRABAJO_PIZARRA_SNAP.md](PLAN_TRABAJO_PIZARRA_SNAP.md)

---

## ✅ Estado actual

Actualmente se encuentran implementados y validados:

### RF01 — Lectura de video

- carga del video;
- apertura mediante OpenCV;
- obtención de FPS;
- resolución;
- cantidad de frames;
- duración.

### RF02 — Procesamiento de frames

- lectura de frames;
- representación mediante arrays de NumPy;
- análisis de `shape`;
- análisis de píxeles;
- canales BGR;
- visualización mediante Matplotlib.

### RF03 — Regiones de interés

Se definieron tres ROI correspondientes a:

- 📸 Captura normal;
- ⭐ Concepto importante;
- 📌 Fin de tema.

Las tres regiones fueron recortadas y validadas visualmente.

### Próxima etapa

**RF04 — Análisis de histogramas**

Responsable principal: **Lucas**.

---

## 📓 Notebook

El notebook principal se encuentra en:

➡️ [notebooks/PizarraSnap.ipynb](notebooks/PizarraSnap.ipynb)

El desarrollo se realiza inicialmente en **Google Colab**.

---

## 🎥 Video de prueba

El proyecto utiliza un video grabado específicamente para desarrollar y validar el sistema.

El archivo no se almacena directamente en GitHub debido a su tamaño.

```text
proyecto_pizzarasnap.mp4
```

El video se comparte con el equipo mediante **Google Drive**:

➡️ [Ver o descargar video de prueba](https://drive.google.com/file/d/1Vcixn88RZXEH3cLLovZQJBfYXKoIKlMb/view?usp=drive_link)

> Para que todos los integrantes puedan acceder, el archivo debe estar compartido en Drive con permisos adecuados para el equipo.

---

## 📁 Estructura actual del repositorio

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

---

## 🔄 Metodología de trabajo

El desarrollo se realizará de forma colaborativa.

Cada módulo deberá:

1. partir de la versión validada del módulo anterior;
2. mantener código claro y comentado;
3. incluir pruebas de funcionamiento;
4. documentar sus entradas y salidas;
5. actualizar la planificación;
6. realizar una revisión antes de integrarse a `main`.

Para reducir conflictos, las nuevas funcionalidades se desarrollarán en ramas independientes y posteriormente se integrarán mediante Pull Requests.

---

## 📚 Conceptos de la Diplomatura aplicados

A lo largo del proyecto se utilizarán, cuando resulten necesarios:

- Python;
- arrays y matrices;
- NumPy;
- píxeles;
- RGB/BGR;
- escala de grises;
- slicing;
- bucles;
- condicionales;
- OpenCV;
- ROI;
- histogramas;
- threshold;
- Gaussian Blur;
- kernels y convolución;
- erosión y dilatación;
- Canny;
- contornos;
- transformaciones de perspectiva;
- procesamiento de imágenes;
- inteligencia artificial aplicada.

---

## 🚧 Estado del proyecto

**En desarrollo.**

La primera etapa correspondiente a video, frames y regiones de interés ya se encuentra completada.

El próximo módulo corresponde al análisis de histogramas y detección de cambios.
