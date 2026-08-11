# 📸 Pizarra Snap

**Sistema inteligente de captura de pizarras mediante visión por computadora.**

Proyecto desarrollado como trabajo colaborativo para la **Diplomatura en Inteligencia Artificial**.

> Última actualización: 11/08/2026.

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
DETECCIÓN DEL CAMBIO
   ↓
IDENTIFICACIÓN Y VALIDACIÓN DEL COMANDO
   ↓
VENTANA DE CAPTURA POSTERIOR
   ↓
EVALUACIÓN DE CALIDAD
   ↓
MEJOR FRAME
   ↓
GUARDADO Y PROCESAMIENTO
   ↓
CLASIFICACIÓN Y ORGANIZACIÓN
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

En etapas posteriores se podrá evaluar incorporar:

- ReportLab o FPDF;
- OCR;
- modelos de visión;
- modelos de lenguaje para generación de resúmenes.

Estas extensiones son complementarias y no deben impedir completar primero el flujo principal.

---

## 👥 Equipo actual

El proyecto está desarrollado por cuatro integrantes:

- **Nicolás**
- **Diego**
- **Walter**
- **Daniela**

---

## 📋 Distribución actual del trabajo

| Integrante | Requerimientos | Responsabilidad | Estado |
|---|---|---|---|
| Nicolás | RF01–RF05 | Video, frames, ROI, histogramas y detección de cambios | RF01–RF05 ✅ |
| Diego | RF06–RF09 | Comandos, validación, ventana temporal y captura posterior | ⬜ Pendiente |
| Walter | RF10–RF12 + RF15 | Calidad, selección, guardado y procesamiento de imagen | ⬜ Pendiente |
| Daniela | RF13–RF14 + RF16 | Clasificación, organización por temas y PDF | ⬜ Pendiente |

La planificación detallada, las entradas y salidas de cada módulo y el registro de avances se encuentran en:

➡️ [PLAN_TRABAJO_PIZARRA_SNAP.md](PLAN_TRABAJO_PIZARRA_SNAP.md)

---

## ✅ Estado actual

### RF01 — Lectura de video

**✅ Realizado**

- carga y apertura del video con OpenCV;
- obtención de FPS;
- resolución;
- cantidad de frames;
- duración.

### RF02 — Procesamiento de frames

**✅ Realizado**

- lectura de frames;
- representación mediante arrays de NumPy;
- análisis de `shape`;
- análisis de píxeles;
- canales BGR;
- visualización mediante Matplotlib.

### RF03 — Regiones de interés

**✅ Realizado**

Se definieron, recortaron y validaron visualmente las tres ROI:

- 📸 Captura normal;
- ⭐ Concepto importante;
- 📌 Fin de tema.

### RF04 — Análisis de histogramas

**✅ Realizado**

- conversión de las ROI a escala de grises;
- aplicación de Gaussian Blur con kernel `5 × 5`;
- cálculo de histogramas;
- normalización L1;
- comparación entre estados libres y cubiertos.

### RF05 — Detección de cambios

**✅ Realizado**

- comparación mediante distancia de Bhattacharyya;
- pruebas libre vs. libre;
- pruebas de transición;
- pruebas de cobertura clara;
- prueba de movimiento cercano;
- calibración experimental del umbral:

```python
umbral_cobertura = 0.40
```

La salida del módulo permite clasificar cada ROI como:

```text
LIBRE
o
CUBIERTA
```

El umbral `0.40` es experimental y podrá requerir calibración si cambian las condiciones de cámara, iluminación o pizarra.

### Próxima etapa

**RF06–RF09 — Identificación y validación de comandos**

Responsable: **Diego**.

---

## 📓 Notebook principal

El notebook oficial del proyecto se encuentra en:

➡️ [notebooks/PizarraSnap.ipynb](notebooks/PizarraSnap.ipynb)

El desarrollo se realiza inicialmente en **Google Colab**.

---

## 🎥 Video de prueba

Archivo utilizado:

```text
proyecto_pizzarasnap.mp4
```

El video no se almacena directamente en GitHub debido a su tamaño. Se comparte mediante **Google Drive**:

➡️ [Ver o descargar video de prueba](https://drive.google.com/file/d/1Vcixn88RZXEH3cLLovZQJBfYXKoIKlMb/view?usp=drive_link)

> El archivo de Drive debe mantenerse con permisos adecuados para los integrantes del equipo.

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

Las carpetas adicionales se crearán solamente cuando el proyecto realmente las necesite, evitando documentar estructuras que todavía no existen.

---

## 🔄 Metodología de trabajo

El desarrollo se realiza de forma secuencial porque cada módulo depende de la salida validada del anterior.

Cada módulo deberá:

1. partir de la versión actualizada de `main`;
2. trabajar en una rama propia;
3. modificar solamente el bloque correspondiente;
4. mantener código simple, claro y comentado;
5. incluir al menos una prueba de funcionamiento;
6. documentar claramente su entrada y su salida;
7. actualizar el plan de trabajo cuando cambie de estado;
8. abrir un Pull Request;
9. pasar una revisión cruzada antes de integrarse a `main`.

### Ramas previstas

```text
feature/rf04-rf05-nicolas
feature/rf06-rf09-diego
feature/rf10-rf12-rf15-walter
feature/rf13-rf14-rf16-daniela
```

---

## 📚 Conceptos de la Diplomatura aplicados

A lo largo del proyecto se utilizarán, cuando aporten valor real:

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

La base correspondiente a **RF01–RF05** está completada y validada.

El módulo de Nicolás entrega a la siguiente etapa el estado de cada ROI como `LIBRE` o `CUBIERTA`.

El desarrollo continúa con **RF06–RF09: identificación del comando, validación de la acción y captura posterior al evento**.
