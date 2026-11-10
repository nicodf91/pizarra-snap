"""Pipeline RF01–RF16 extraído del notebook canónico de Pizarra Snap."""

from datetime import datetime
from functools import partial
from io import BytesIO
import math
from pathlib import Path
import tempfile
import warnings
from xml.sax.saxutils import escape

import cv2
import numpy as np
from PIL import Image as PILImage, ImageDraw, ImageFilter
from pypdf import PdfReader
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.platypus import (
    Image as RLImage,
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


# RF01–RF05 · Nicolás. Coordenadas (x1, x2, y1, y2) del notebook.
COORDENADAS_ROI = {
    "CAPTURA_NORMAL": (75, 210, 190, 300),
    "CONCEPTO_IMPORTANTE": (75, 210, 400, 510),
    "FIN_DE_TEMA": (75, 215, 585, 740),
}
UMBRAL_COBERTURA = 0.40


# Creo una función que prepara una ROI y devuelve
# su histograma normalizado listo para comparar.

def calcular_histograma_roi(roi):

    # Convierto la ROI de BGR a escala de grises.
    roi_gris = cv2.cvtColor(
        roi,
        cv2.COLOR_BGR2GRAY
    )

    # Aplico el mismo suavizado Gaussiano utilizado anteriormente.
    roi_suavizada = cv2.GaussianBlur(
        roi_gris,
        (5, 5),
        0
    )

    # Calculo el histograma de intensidades de 0 a 255.
    histograma = cv2.calcHist(
        [roi_suavizada],
        [0],
        None,
        [256],
        [0, 256]
    )

    # Normalizo el histograma para trabajar con proporciones.
    histograma_normalizado = cv2.normalize(
        histograma,
        None,
        alpha=1,
        beta=0,
        norm_type=cv2.NORM_L1
    )

    # Devuelvo el histograma en formato float32,
    # listo para utilizar con cv2.compareHist().
    return histograma_normalizado.astype(np.float32)


def _obtener_roi_en_segundo(video, fps, segundo, x1, x2, y1, y2):
    numero_frame = int(segundo * fps)
    if not video.set(cv2.CAP_PROP_POS_FRAMES, numero_frame):
        raise ValueError(f"No se pudo posicionar el video en el segundo {segundo}.")

    leido, frame = video.read()
    if not leido:
        raise ValueError(f"No se pudo leer el frame de referencia del segundo {segundo}.")
    if y2 > frame.shape[0] or x2 > frame.shape[1]:
        raise ValueError("La resolución del video no contiene las ROI del notebook.")

    return frame[y1:y2, x1:x2]


def clasificar_estado_roi(distancia, umbral=UMBRAL_COBERTURA):
    if distancia >= umbral:
        return "CUBIERTA"
    return "LIBRE"


# RF06–RF09 · Diego.
def _detectar_capturas(video, fps, total_frames):
    segundo_inicio = 0.5
    rois = {
        evento: {
            "coords": coords,
            "hist_referencia": calcular_histograma_roi(
                _obtener_roi_en_segundo(video, fps, segundo_inicio, *coords)
            ),
        }
        for evento, coords in COORDENADAS_ROI.items()
    }

    duracion_minima_valida = 0.5
    duracion_maxima_valida = 4.0
    ventana_frames = int(2.0 * fps)  # RF08: ~2 segundos de frames, calculados con el fps real

    if not video.set(cv2.CAP_PROP_POS_FRAMES, 0):
        raise ValueError("No se pudo volver al inicio del video.")

    estado_anterior = {evento: "LIBRE" for evento in rois}
    evento_en_curso = {evento: None for evento in rois}
    recolectando = {}  # RF09: evento -> ventana de captura en curso
    capturas = []      # capturas ya cerradas, listas para entregarle a Walter

    numero_frame = 0
    frame_limite = total_frames

    while numero_frame < frame_limite:
        ret, frame = video.read()
        if not ret:
            break

        segundo_actual = numero_frame / fps

        estados_actuales = {}
        for evento, datos in rois.items():
            x1, x2, y1, y2 = datos["coords"]
            roi = frame[y1:y2, x1:x2]
            histograma = calcular_histograma_roi(roi)
            distancia = cv2.compareHist(datos["hist_referencia"], histograma, cv2.HISTCMP_BHATTACHARYYA)
            estados_actuales[evento] = clasificar_estado_roi(distancia)

        cantidad_cubiertas = list(estados_actuales.values()).count("CUBIERTA")

        for evento, estado_actual in estados_actuales.items():

            if estado_anterior[evento] == "LIBRE" and estado_actual == "CUBIERTA":
                evento_en_curso[evento] = segundo_actual if cantidad_cubiertas == 1 else None

            if estado_anterior[evento] == "CUBIERTA" and estado_actual == "LIBRE":
                if evento_en_curso[evento] is not None:
                    inicio = evento_en_curso[evento]
                    duracion_evento = segundo_actual - inicio
                    if duracion_minima_valida <= duracion_evento <= duracion_maxima_valida:
                        # RF08: abro la ventana posterior al evento.
                        recolectando[evento] = {
                            "frames_restantes": ventana_frames,
                            "frames_candidatos": [],
                            "momento_del_evento": segundo_actual,
                        }
                evento_en_curso[evento] = None

            estado_anterior[evento] = estado_actual

        # RF09: si hay ventanas abiertas, junto el frame actual en cada una.
        for evento in list(recolectando.keys()):
            info = recolectando[evento]
            info["frames_candidatos"].append(frame.copy())
            info["frames_restantes"] -= 1

            if info["frames_restantes"] <= 0:
                capturas.append({
                    "tipo_evento": evento,
                    "momento_del_evento": info["momento_del_evento"],
                    "frames_candidatos": info["frames_candidatos"],
                })
                del recolectando[evento]

        numero_frame += 1
    if numero_frame == 0:
        raise ValueError("No se pudo leer el primer frame del video.")
    return capturas


# RF10–RF12 y RF15 · aporte de Walter integrado en el notebook.
PESOS_CALIDAD = {
    "nitidez": 0.55,
    "estabilidad": 0.30,
    "contraste": 0.15,
}


def _normalizar_valores(valores, mayor_es_mejor=True):
    """Normaliza una métrica dentro de la ventana del evento."""
    minimo = min(valores)
    maximo = max(valores)
    rango = maximo - minimo

    if rango <= 1e-12:
        return [0.5] * len(valores)

    if mayor_es_mejor:
        return [(valor - minimo) / rango for valor in valores]
    return [(maximo - valor) / rango for valor in valores]


def evaluar_calidad_frames(frames_candidatos, escala_metricas=0.5):
    """RF10: calcula nitidez, contraste, movimiento, estabilidad y score."""
    if not frames_candidatos:
        raise ValueError("frames_candidatos no puede estar vacío.")
    if not 0 < escala_metricas <= 1:
        raise ValueError("escala_metricas debe estar entre 0 y 1.")

    evaluaciones = []
    gris_anterior = None

    for indice, frame_candidato in enumerate(frames_candidatos):
        if not isinstance(frame_candidato, np.ndarray) or frame_candidato.ndim != 3:
            raise ValueError(f"El candidato {indice} no es un frame BGR válido.")

        gris = cv2.cvtColor(frame_candidato, cv2.COLOR_BGR2GRAY)
        if escala_metricas < 1:
            gris_metrica = cv2.resize(
                gris,
                None,
                fx=escala_metricas,
                fy=escala_metricas,
                interpolation=cv2.INTER_AREA,
            )
        else:
            gris_metrica = gris

        # Aplico un filtro Laplaciano y calculo su varianza como medida de nitidez.
        # Cuanto mayor la varianza, más nítida la imagen y menor el desenfoque por movimiento.
        nitidez = float(cv2.Laplacian(gris_metrica, cv2.CV_64F).var())
        # Calculo el contraste como la desviación estándar de las intensidades de píxeles.
        # Un mayor valor indica mayor contraste.
        contraste = float(gris_metrica.std())
        movimiento = None
        if gris_anterior is not None:
            movimiento = float(cv2.absdiff(gris_metrica, gris_anterior).mean())

        evaluaciones.append({
            "indice_frame": indice,
            "nitidez": nitidez,
            "contraste": contraste,
            "movimiento": movimiento,
        })
        gris_anterior = gris_metrica

    # El primer frame se compara con su vecino para no premiarlo con movimiento cero artificial.
    if len(evaluaciones) == 1:
        evaluaciones[0]["movimiento"] = 0.0
    else:
        evaluaciones[0]["movimiento"] = evaluaciones[1]["movimiento"]

    nitideces = [item["nitidez"] for item in evaluaciones]
    contrastes = [item["contraste"] for item in evaluaciones]
    movimientos = [item["movimiento"] for item in evaluaciones]

    nitidez_normalizada = _normalizar_valores(nitideces)
    contraste_normalizado = _normalizar_valores(contrastes)
    estabilidad_normalizada = _normalizar_valores(movimientos, mayor_es_mejor=False)

    for indice, evaluacion in enumerate(evaluaciones):
        evaluacion["nitidez_normalizada"] = nitidez_normalizada[indice]
        evaluacion["contraste_normalizado"] = contraste_normalizado[indice]
        evaluacion["estabilidad"] = estabilidad_normalizada[indice]
        evaluacion["score"] = (
            PESOS_CALIDAD["nitidez"] * nitidez_normalizada[indice]
            + PESOS_CALIDAD["estabilidad"] * estabilidad_normalizada[indice]
            + PESOS_CALIDAD["contraste"] * contraste_normalizado[indice]
        )

    return evaluaciones


def seleccionar_mejor_frame(frames_candidatos):
    """RF11: devuelve un único ganador y las métricas que justifican la elección."""
    evaluaciones = evaluar_calidad_frames(frames_candidatos)
    indice_ganador = max(
        range(len(evaluaciones)),
        key=lambda indice: (
            evaluaciones[indice]["score"],
            evaluaciones[indice]["nitidez"],
            -evaluaciones[indice]["movimiento"],
            -indice,
        ),
    )

    return (
        frames_candidatos[indice_ganador],
        indice_ganador,
        dict(evaluaciones[indice_ganador]),
        evaluaciones,
    )


def mejorar_captura(frame_bgr, ganancia_minima_contraste=1.05, retencion_minima_nitidez=0.90):
    """RF15: genera una copia gris con CLAHE solo si la medición justifica usarla."""
    gris = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    procesada = clahe.apply(gris)

    contraste_original = float(gris.std())
    contraste_procesado = float(procesada.std())
    nitidez_original = float(cv2.Laplacian(gris, cv2.CV_64F).var())
    nitidez_procesada = float(cv2.Laplacian(procesada, cv2.CV_64F).var())

    ganancia_contraste = contraste_procesado / max(contraste_original, 1e-12)
    retencion_nitidez = nitidez_procesada / max(nitidez_original, 1e-12)
    aplicar = (
        ganancia_contraste >= ganancia_minima_contraste
        and retencion_nitidez >= retencion_minima_nitidez
    )

    evaluacion = {
        "metodo": "escala_grises_clahe",
        "contraste_original": contraste_original,
        "contraste_procesado": contraste_procesado,
        "ganancia_contraste": ganancia_contraste,
        "nitidez_original": nitidez_original,
        "nitidez_procesada": nitidez_procesada,
        "retencion_nitidez": retencion_nitidez,
        "aplicado": aplicar,
    }
    return (procesada if aplicar else None), evaluacion


def guardar_imagen(imagen, ruta):
    """RF12: guarda una imagen y falla explícitamente si OpenCV no puede escribirla."""
    ruta = Path(ruta)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    if not cv2.imwrite(str(ruta), imagen):
        raise IOError(f"No se pudo guardar la imagen en {ruta}.")
    return str(ruta.resolve())


def procesar_capturas(capturas_entrada, directorio_salida, liberar_frames_candidatos=True):
    """Integra RF10, RF11, RF12 y RF15 sobre la salida real de Diego."""
    eventos_validos = {"CAPTURA_NORMAL", "CONCEPTO_IMPORTANTE", "FIN_DE_TEMA"}
    directorio_salida = Path(directorio_salida)
    resultados = []

    for numero_captura, captura in enumerate(capturas_entrada, start=1):
        tipo_evento = captura["tipo_evento"]
        momento_del_evento = float(captura["momento_del_evento"])
        frames_candidatos = captura["frames_candidatos"]

        if tipo_evento not in eventos_validos:
            raise ValueError(f"tipo_evento desconocido: {tipo_evento}")
        if not isinstance(frames_candidatos, list):
            raise ValueError("frames_candidatos debe ser una lista.")

        mejor_frame, indice_ganador, metricas_ganador, evaluaciones = seleccionar_mejor_frame(
            frames_candidatos
        )

        momento_ms = round(momento_del_evento * 1000)
        nombre_base = (
            f"captura_{numero_captura:03d}_{tipo_evento.lower()}_{momento_ms:06d}ms"
        )
        captura_path = guardar_imagen(
            mejor_frame,
            directorio_salida / f"{nombre_base}.png",
        )

        captura_procesada, evaluacion_procesamiento = mejorar_captura(mejor_frame)
        captura_procesada_path = None
        procesamiento_aplicado = None
        if captura_procesada is not None:
            captura_procesada_path = guardar_imagen(
                captura_procesada,
                directorio_salida / f"{nombre_base}_procesada.png",
            )
            procesamiento_aplicado = evaluacion_procesamiento["metodo"]

        resultados.append({
            "numero_captura": numero_captura,
            "tipo_evento": tipo_evento,
            "momento_del_evento": momento_del_evento,
            "indice_mejor_frame": indice_ganador,
            "mejor_frame": mejor_frame,
            "metricas_mejor_frame": metricas_ganador,
            "evaluaciones_calidad": evaluaciones,
            "captura_path": captura_path,
            "captura_procesada": captura_procesada,
            "captura_procesada_path": captura_procesada_path,
            "procesamiento_aplicado": procesamiento_aplicado,
            "evaluacion_procesamiento": evaluacion_procesamiento,
        })

        # RF09 ya terminó: libero referencias a los candidatos y conservo solo el ganador.
        if liberar_frames_candidatos:
            frames_candidatos.clear()

    return resultados


# RF13–RF14 y RF16 · Daniela.
CATEGORIA_POR_EVENTO = {
    "CAPTURA_NORMAL": "NORMAL",
    "CONCEPTO_IMPORTANTE": "IMPORTANTE",
    "FIN_DE_TEMA": "FIN_DE_TEMA",
}


def seleccionar_imagen_reporte(resultado_walter):
    """Selecciona una ruta persistida: procesada, original o ninguna."""
    candidatos = (
        ("captura_procesada_path", "procesada"),
        ("captura_path", "original"),
    )

    for campo, fuente in candidatos:
        valor = resultado_walter.get(campo)
        if valor is None:
            continue
        if not isinstance(valor, (str, Path)):
            warnings.warn(
                f"{campo} debe ser str o Path; se recibió {type(valor).__name__}.",
                RuntimeWarning,
                stacklevel=2,
            )
            continue

        ruta = Path(valor).expanduser()
        if ruta.is_file():
            return str(ruta.resolve()), fuente

        warnings.warn(
            f"No existe la imagen declarada en {campo}: {ruta}",
            RuntimeWarning,
            stacklevel=2,
        )

    warnings.warn(
        f"La captura {resultado_walter.get('numero_captura', '?')} no tiene una imagen utilizable.",
        RuntimeWarning,
        stacklevel=2,
    )
    return None, "sin_imagen"


def adaptar_para_reporte(resultados_walter_entrada):
    """RF13: crea registros livianos y serializables para RF14 y RF16."""
    if resultados_walter_entrada is None:
        raise ValueError("resultados_walter no puede ser None.")

    resultados_reporte = []
    campos_obligatorios = {
        "numero_captura",
        "tipo_evento",
        "momento_del_evento",
    }

    for posicion, resultado in enumerate(resultados_walter_entrada):
        if not isinstance(resultado, dict):
            raise ValueError(f"El resultado en posición {posicion} debe ser un dict.")

        faltantes = campos_obligatorios - resultado.keys()
        if faltantes:
            raise ValueError(
                f"Resultado de Walter incompleto en posición {posicion}: {sorted(faltantes)}"
            )

        numero_captura = resultado["numero_captura"]
        if not isinstance(numero_captura, int) or isinstance(numero_captura, bool):
            raise ValueError("numero_captura debe ser un entero.")

        tipo_evento = resultado["tipo_evento"]
        if tipo_evento not in CATEGORIA_POR_EVENTO:
            raise ValueError(
                f"tipo_evento desconocido en captura {numero_captura}: {tipo_evento!r}"
            )

        try:
            momento_del_evento = float(resultado["momento_del_evento"])
        except (TypeError, ValueError) as exc:
            raise ValueError(
                f"momento_del_evento inválido en captura {numero_captura}."
            ) from exc

        imagen_path, fuente_imagen = seleccionar_imagen_reporte(resultado)
        resultados_reporte.append({
            "numero_captura": numero_captura,
            "tipo_evento": tipo_evento,
            "categoria": CATEGORIA_POR_EVENTO[tipo_evento],
            "momento_del_evento": momento_del_evento,
            "imagen_path": imagen_path,
            "fuente_imagen": fuente_imagen,
        })

    return resultados_reporte


def agrupar_por_temas(resultados_reporte_entrada):
    """RF14: agrupa capturas en orden, sin mutar la entrada ni perder registros."""
    if resultados_reporte_entrada is None:
        raise ValueError("resultados_reporte no puede ser None.")

    capturas_entrada = list(resultados_reporte_entrada)
    if not capturas_entrada:
        return []

    temas = []
    capturas_tema_actual = []
    numeros_vistos = set()
    numero_tema = 1

    for posicion, captura in enumerate(capturas_entrada):
        if not isinstance(captura, dict):
            raise ValueError(f"La captura en posición {posicion} debe ser un dict.")

        faltantes = {"numero_captura", "tipo_evento", "categoria"} - captura.keys()
        if faltantes:
            raise ValueError(f"Captura incompleta en posición {posicion}: {sorted(faltantes)}")

        numero_captura = captura["numero_captura"]
        if numero_captura in numeros_vistos:
            raise ValueError(f"numero_captura duplicado: {numero_captura}")
        numeros_vistos.add(numero_captura)

        tipo_evento = captura["tipo_evento"]
        if tipo_evento not in CATEGORIA_POR_EVENTO:
            raise ValueError(f"tipo_evento desconocido: {tipo_evento!r}")
        if captura["categoria"] != CATEGORIA_POR_EVENTO[tipo_evento]:
            raise ValueError(
                f"Categoría incoherente en captura {numero_captura}: {captura['categoria']!r}"
            )

        capturas_tema_actual.append(dict(captura))
        if tipo_evento == "FIN_DE_TEMA":
            temas.append({
                "numero_tema": numero_tema,
                "capturas": capturas_tema_actual,
                "cerrado": True,
            })
            numero_tema += 1
            capturas_tema_actual = []

    if capturas_tema_actual:
        temas.append({
            "numero_tema": numero_tema,
            "capturas": capturas_tema_actual,
            "cerrado": False,
        })

    capturas_salida = [captura for tema in temas for captura in tema["capturas"]]
    if len(capturas_salida) != len(capturas_entrada):
        raise RuntimeError("RF14 perdió o duplicó capturas durante la agrupación.")

    return temas


# Importo las herramientas de ReportLab para construir el PDF.

# --- Paleta de colores de Pizarra Snap (Identidad V1) ---

COLOR_FONDO = colors.HexColor("#FAFAFA")             # fondo general claro
COLOR_PRIMARIO = colors.HexColor("#157A6E")           # teal: estructura, símbolo, títulos
COLOR_ACENTO = colors.HexColor("#F5A623")             # ámbar: destello del logo y CONCEPTO IMPORTANTE
COLOR_TEXTO = colors.HexColor("#1A1A1A")              # texto principal
COLOR_TEXTO_SECUNDARIO = colors.HexColor("#6B7280")   # texto secundario / metadatos
COLOR_BORDE = colors.HexColor("#E5E7EB")              # líneas divisorias, bordes suaves

# --- Tipografía base (fuentes estándar de ReportLab, sin archivos externos) ---

FUENTE_TITULO = "Helvetica-Bold"
FUENTE_TAGLINE = "Helvetica-Oblique"
FUENTE_TEXTO = "Helvetica"

# Se conservan los datos originales de la portada de Daniela.
# Solamente cambian la institución y la materia, según lo acordado.
DATOS_PORTADA_DANIELA = {
    "titulo_clase": "Clase de prueba — Pizarra Snap",
    "institucion": "UTN",
    "docente": "Lic. Manuela Pérez",
    "materia": "DIPLOMATURA EN IA",
    "curso": "7° Tec. Programación",
    "unidad_tematica": "Introducción a las organizaciones",
    "clase_numero": "1",
}


# --- Generación del fondo de marca: degradados suaves + cinta con brillo ---
# Se genera UNA sola vez y se reutiliza como imagen de fondo en portada
# y en las páginas de contenido.

ANCHO_PX, ALTO_PX = 1240, 1754  # proporción A4 a 150dpi

def _bezier(p0, p1, p2, p3, t):
    mt = 1 - t
    x = mt**3*p0[0] + 3*mt**2*t*p1[0] + 3*mt*t**2*p2[0] + t**3*p3[0]
    y = mt**3*p0[1] + 3*mt**2*t*p1[1] + 3*mt*t**2*p2[1] + t**3*p3[1]
    return (x, y)

def _dibujar_cinta(draw, p0, p1, p2, p3, color_base, ancho_max=90, n=300):
    puntos = [_bezier(p0, p1, p2, p3, i/n) for i in range(n+1)]
    for i in range(len(puntos)-1):
        t = i/len(puntos)
        w = ancho_max * (0.35 + 0.65*abs(math.sin(t*math.pi*2.2 + 0.6)))
        x0, y0 = puntos[i]
        x1, y1 = puntos[i+1]
        dx, dy = x1-x0, y1-y0
        largo = math.hypot(dx, dy) or 1
        nx, ny = -dy/largo, dx/largo
        brillo = max(0, math.sin(t*math.pi*3.5))
        alpha = int(20 + brillo*40)
        r = int(color_base[0] + (255-color_base[0])*brillo*0.5)
        g = int(color_base[1] + (255-color_base[1])*brillo*0.5)
        b = int(color_base[2] + (255-color_base[2])*brillo*0.5)
        poligono = [
            (x0+nx*w/2, y0+ny*w/2), (x1+nx*w/2, y1+ny*w/2),
            (x1-nx*w/2, y1-ny*w/2), (x0-nx*w/2, y0-ny*w/2),
        ]
        draw.polygon(poligono, fill=(r, g, b, alpha))

def generar_fondo_marca(nombre_archivo, blobs, cintas, base_color=(250, 250, 250)):
    """
    blobs: lista de (cx, cy, radio) para los degradados suaves.
    cintas: lista de (p0, p1, p2, p3, color_rgb, ancho_max) para las vetas con brillo.
    """
    img = PILImage.new("RGB", (ANCHO_PX, ALTO_PX), base_color)

    capa_blobs = PILImage.new("RGBA", (ANCHO_PX, ALTO_PX), (0, 0, 0, 0))
    dibujo_blobs = ImageDraw.Draw(capa_blobs)
    colores_ciclo = [(21,122,110,55), (245,166,35,45), (21,122,110,35)]
    for (cx, cy, r), color in zip(blobs, colores_ciclo * 3):
        dibujo_blobs.ellipse([cx-r, cy-r, cx+r, cy+r], fill=color)
    capa_blobs = capa_blobs.filter(ImageFilter.GaussianBlur(130))
    img = PILImage.alpha_composite(img.convert("RGBA"), capa_blobs)

    capa_cintas = PILImage.new("RGBA", (ANCHO_PX, ALTO_PX), (0, 0, 0, 0))
    dibujo_cintas = ImageDraw.Draw(capa_cintas)
    for p0, p1, p2, p3, color, ancho in cintas:
        _dibujar_cinta(dibujo_cintas, p0, p1, p2, p3, color, ancho)
    capa_cintas = capa_cintas.filter(ImageFilter.GaussianBlur(12))
    img = PILImage.alpha_composite(img, capa_cintas).convert("RGB")

    img.save(nombre_archivo, quality=95)
    return nombre_archivo

TEAL_RGB = (21, 122, 110)
AMBAR_RGB = (245, 166, 35)

def _crear_fondos_marca_temporales(directorio):
    """Reproduce los fondos originales de Daniela fuera del repositorio."""
    directorio = Path(directorio)
    fondo_portada = directorio / "fondo_portada.png"
    fondo_contenido = directorio / "fondo_contenido.png"
    generar_fondo_marca(
        fondo_portada,
        blobs=[(150,120,340), (1080,250,360), (120,1550,320), (1120,1650,280)],
        cintas=[
            ((-150,-100), (250,450), (-100,950), (300,ALTO_PX+150), TEAL_RGB, 100),
            ((ANCHO_PX+150,150), (ANCHO_PX-400,600), (ANCHO_PX+200,1150), (ANCHO_PX-250,ALTO_PX+200), AMBAR_RGB, 65),
        ],
    )
    generar_fondo_marca(
        fondo_contenido,
        blobs=[(-60,-60,280), (1300,80,300), (-90,1750,280), (1310,1700,260)],
        cintas=[
            ((-150,-100), (250,450), (-100,950), (300,ALTO_PX+150), TEAL_RGB, 80),
            ((ANCHO_PX+150,150), (ANCHO_PX-400,600), (ANCHO_PX+200,1150), (ANCHO_PX-250,ALTO_PX+200), AMBAR_RGB, 50),
        ],
    )
    return fondo_portada, fondo_contenido


def dibujar_simbolo(c, x, y, tamano):
    """
    Dibuja el símbolo de Pizarra Snap: cuatro marcas de encuadre
    y un destello, centrado en (x, y). 'tamano' es el lado del cuadrado.
    """
    longitud_marca = tamano * 0.30
    grosor = max(1.4, tamano * 0.045)
    mitad = tamano / 2

    c.saveState()
    c.setStrokeColor(COLOR_PRIMARIO)
    c.setLineWidth(grosor)
    c.setLineCap(1)  # extremos redondeados

    # Esquina superior izquierda
    c.line(x - mitad, y + mitad, x - mitad + longitud_marca, y + mitad)
    c.line(x - mitad, y + mitad, x - mitad, y + mitad - longitud_marca)

    # Esquina superior derecha
    c.line(x + mitad, y + mitad, x + mitad - longitud_marca, y + mitad)
    c.line(x + mitad, y + mitad, x + mitad, y + mitad - longitud_marca)

    # Esquina inferior izquierda
    c.line(x - mitad, y - mitad, x - mitad + longitud_marca, y - mitad)
    c.line(x - mitad, y - mitad, x - mitad, y - mitad + longitud_marca)

    # Esquina inferior derecha
    c.line(x + mitad, y - mitad, x + mitad - longitud_marca, y - mitad)
    c.line(x + mitad, y - mitad, x + mitad, y - mitad + longitud_marca)

    # Destello (rombo) en la esquina superior derecha, color acento.
    r = tamano * 0.12
    cx, cy = x + mitad, y + mitad

    path = c.beginPath()
    path.moveTo(cx, cy + r)
    path.lineTo(cx + r, cy)
    path.lineTo(cx, cy - r)
    path.lineTo(cx - r, cy)
    path.close()

    c.setFillColor(COLOR_ACENTO)
    c.drawPath(path, fill=1, stroke=0)

    c.restoreState()


def dibujar_wordmark(c, x, y, tamano_fuente, alineacion="left"):
    """
    Dibuja 'Pizarra' (gris carbón) + 'Snap' (ámbar).
    (x, y) es el punto base, según la alineación elegida.
    """
    c.saveState()

    texto1 = "Pizarra "
    texto2 = "Snap"
    ancho1 = stringWidth(texto1, FUENTE_TITULO, tamano_fuente)
    ancho2 = stringWidth(texto2, FUENTE_TITULO, tamano_fuente)
    ancho_total = ancho1 + ancho2

    if alineacion == "center":
        x_inicio = x - ancho_total / 2
    elif alineacion == "right":
        x_inicio = x - ancho_total
    else:
        x_inicio = x

    c.setFont(FUENTE_TITULO, tamano_fuente)
    c.setFillColor(COLOR_TEXTO)
    c.drawString(x_inicio, y, texto1)

    c.setFillColor(COLOR_ACENTO)
    c.drawString(x_inicio + ancho1, y, texto2)

    c.restoreState()
    return ancho_total


def logo_portada(c, cx, top_y):
    """
    Versión protagonista del logo: símbolo grande + wordmark + tagline.
    (cx, top_y) = centro horizontal y posición vertical superior del símbolo.
    """
    tam_simbolo = 30 * mm
    dibujar_simbolo(c, cx, top_y, tam_simbolo)

    y_wordmark = top_y - tam_simbolo / 2 - 14 * mm
    dibujar_wordmark(c, cx, y_wordmark, 30, alineacion="center")

    y_tagline = y_wordmark - 9 * mm
    c.saveState()
    c.setFont(FUENTE_TAGLINE, 11)
    c.setFillColor(COLOR_TEXTO_SECUNDARIO)
    texto_tag = "La pizarra que recuerda tu clase."
    ancho_tag = stringWidth(texto_tag, FUENTE_TAGLINE, 11)
    c.drawString(cx - ancho_tag / 2, y_tagline, texto_tag)
    c.restoreState()


def logo_header(c, x, y, alineacion="left"):
    """
    Versión chica del logo: símbolo + wordmark en una línea.
    Pensada para encabezado o pie de página.
    """
    tam_simbolo = 5.5 * mm
    tam_fuente = 10

    if alineacion == "left":
        cx_simbolo = x + tam_simbolo / 2
        x_texto = x + tam_simbolo + 2.5 * mm
        dibujar_simbolo(c, cx_simbolo, y + 1, tam_simbolo)
        dibujar_wordmark(c, x_texto, y - 2, tam_fuente, alineacion="left")
    else:  # center
        ancho_texto_aprox = stringWidth("Pizarra Snap", FUENTE_TITULO, tam_fuente)
        ancho_total = tam_simbolo + 2.5 * mm + ancho_texto_aprox
        x_inicio = x - ancho_total / 2
        cx_simbolo = x_inicio + tam_simbolo / 2
        dibujar_simbolo(c, cx_simbolo, y + 1, tam_simbolo)
        dibujar_wordmark(c, x_inicio + tam_simbolo + 2.5 * mm, y - 2, tam_fuente, alineacion="left")


def encabezado_pie_pagina(canvas_pagina, documento, fondo_contenido_path):
    canvas_pagina.saveState()
    ancho_pagina, alto_pagina = A4

    canvas_pagina.drawImage(str(fondo_contenido_path), 0, 0, width=ancho_pagina, height=alto_pagina)

    logo_header(canvas_pagina, 20 * mm, alto_pagina - 15 * mm, alineacion="left")

    canvas_pagina.setStrokeColor(COLOR_BORDE)
    canvas_pagina.setLineWidth(0.5)
    canvas_pagina.line(20 * mm, alto_pagina - 20 * mm, ancho_pagina - 20 * mm, alto_pagina - 20 * mm)

    canvas_pagina.setFont(FUENTE_TEXTO, 8)
    canvas_pagina.setFillColor(COLOR_TEXTO_SECUNDARIO)
    canvas_pagina.drawCentredString(ancho_pagina / 2, 10 * mm, f"Pizarra Snap — página {documento.page}")

    canvas_pagina.restoreState()


def dibujar_portada(canvas_pagina, documento, fecha_clase=None, titulo_clase=None,
                     institucion=None, docente=None, materia=None, curso=None,
                     unidad_tematica=None, clase_numero=None, fondo_portada_path=None):
    canvas_pagina.saveState()
    ancho_pagina, alto_pagina = A4

    canvas_pagina.drawImage(str(fondo_portada_path), 0, 0, width=ancho_pagina, height=alto_pagina)

    logo_portada(canvas_pagina, ancho_pagina / 2, alto_pagina - 90 * mm)

    canvas_pagina.setStrokeColor(COLOR_BORDE)
    canvas_pagina.setLineWidth(0.5)
    canvas_pagina.line(50 * mm, alto_pagina - 150 * mm, ancho_pagina - 50 * mm, alto_pagina - 150 * mm)

    if fecha_clase is None:
        fecha_clase = datetime.now().strftime("%d/%m/%Y")

    if titulo_clase:
        canvas_pagina.setFont(FUENTE_TEXTO, 11)
        canvas_pagina.setFillColor(COLOR_TEXTO_SECUNDARIO)
        canvas_pagina.drawCentredString(ancho_pagina / 2, alto_pagina - 163 * mm, titulo_clase)

    # --- Ficha de datos, alineada a la izquierda ---
    # Etiqueta en mayúscula (verde) arriba, contenido tal como se escribió, debajo.
    campos = [
        ("Institución", institucion), ("Docente", docente), ("Materia", materia),
        ("Curso", curso), ("Unidad temática", unidad_tematica),
        ("Clase N°", clase_numero), ("Fecha", fecha_clase),
    ]
    campos_completos = [(l, v) for l, v in campos if v]

    if campos_completos:
        card_w = 130 * mm
        card_h = 12*mm + len(campos_completos) * 13*mm
        card_x = (ancho_pagina - card_w) / 2
        card_y = alto_pagina - 175*mm - card_h

        canvas_pagina.setFillColor(colors.white)
        canvas_pagina.setStrokeColor(COLOR_BORDE)
        canvas_pagina.setLineWidth(0.7)
        canvas_pagina.roundRect(card_x, card_y, card_w, card_h, 4*mm, fill=1, stroke=1)

        fy = card_y + card_h - 12*mm
        for label, valor in campos_completos:
            canvas_pagina.setFont(FUENTE_TITULO, 9)
            canvas_pagina.setFillColor(COLOR_PRIMARIO)
            canvas_pagina.drawString(card_x + 10*mm, fy, label.upper())

            canvas_pagina.setFont(FUENTE_TEXTO, 10)
            canvas_pagina.setFillColor(COLOR_TEXTO_SECUNDARIO)
            canvas_pagina.drawString(card_x + 10*mm, fy - 5.5*mm, str(valor))

            fy -= 13*mm

    canvas_pagina.restoreState()


# --- Estilos de texto reutilizables para el contenido del PDF ---

estilos = getSampleStyleSheet()

estilo_titulo_tema = ParagraphStyle(
    "TituloTema",
    parent=estilos["Heading1"],
    fontName=FUENTE_TITULO,
    fontSize=18,
    textColor=COLOR_PRIMARIO,
    spaceAfter=6 * mm,
    spaceBefore=4 * mm,
)

estilo_etiqueta_categoria = ParagraphStyle(
    "EtiquetaCategoria",
    parent=estilos["Normal"],
    fontName=FUENTE_TITULO,
    fontSize=10,
    textColor=COLOR_TEXTO,
    spaceAfter=1 * mm,
)

estilo_etiqueta_importante = ParagraphStyle(
    "EtiquetaImportante",
    parent=estilos["Normal"],
    fontName=FUENTE_TITULO,
    fontSize=10,
    textColor=COLOR_ACENTO,
    spaceAfter=1 * mm,
)

estilo_metadato = ParagraphStyle(
    "Metadato",
    parent=estilos["Normal"],
    fontName=FUENTE_TEXTO,
    fontSize=8,
    textColor=COLOR_TEXTO_SECUNDARIO,
)


def _texto_pdf(valor):
    return escape(str(valor))


def _placeholder_imagen_pdf(ancho, alto, detalle=None):
    texto = "Imagen no disponible"
    if detalle:
        texto += f"<br/><font size='7'>{_texto_pdf(detalle)}</font>"
    tabla = Table([[Paragraph(texto, ParagraphStyle(
        "PlaceholderDaniela", parent=estilo_metadato, alignment=TA_CENTER,
    ))]], colWidths=[ancho], rowHeights=[alto])
    tabla.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#E5E7EB")),
        ("TEXTCOLOR", (0, 0), (-1, -1), COLOR_TEXTO_SECUNDARIO),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    return tabla


def _imagen_para_pdf(registro, ancho_maximo, alto_maximo=96 * mm):
    """Carga una imagen validada y conserva su relación de aspecto."""
    imagen_path = registro.get("imagen_path")
    alto_placeholder = min(alto_maximo, ancho_maximo * 9 / 16)
    if not imagen_path:
        return _placeholder_imagen_pdf(ancho_maximo, alto_placeholder, "La captura no tiene un archivo utilizable.")
    try:
        ruta = Path(imagen_path)
        with PILImage.open(ruta) as imagen_pil:
            imagen_pil.load()
            ancho_original, alto_original = imagen_pil.size
            if ancho_original <= 0 or alto_original <= 0:
                raise ValueError("La imagen no tiene dimensiones válidas.")
            buffer = BytesIO()
            imagen_pil.convert("RGB").save(buffer, format="PNG")
        escala = min(ancho_maximo / ancho_original, alto_maximo / alto_original)
        return RLImage(BytesIO(buffer.getvalue()), width=ancho_original * escala, height=alto_original * escala)
    except (OSError, ValueError, TypeError) as exc:
        warnings.warn(
            f"No se pudo abrir la imagen de la captura {registro.get('numero_captura', '?')}: {exc}",
            RuntimeWarning, stacklevel=2,
        )
        return _placeholder_imagen_pdf(ancho_maximo, alto_placeholder, "El archivo existe pero no pudo abrirse.")


COLOR_RENGLON = colors.HexColor("#B8C4C2")

def crear_tarjeta_captura(registro, ancho_imagen):
    categoria = registro["categoria"]
    es_importante = categoria == "IMPORTANTE"
    es_cierre = categoria == "FIN_DE_TEMA"

    contenido_imagen = _imagen_para_pdf(registro, ancho_imagen)

    if es_importante:
        texto_etiqueta, estilo_etiqueta = "⭐ CONCEPTO IMPORTANTE", estilo_etiqueta_importante
    elif es_cierre:
        texto_etiqueta, estilo_etiqueta = "📌 FIN DE TEMA", estilo_etiqueta_categoria
    else:
        texto_etiqueta, estilo_etiqueta = "📸 CAPTURA", estilo_etiqueta_categoria

    etiqueta = Paragraph(texto_etiqueta, estilo_etiqueta)
    metadato = Paragraph(f"Momento: {registro['momento_del_evento']}s", estilo_metadato)

    fila_pie = Table([[etiqueta, metadato]], colWidths=[ancho_imagen * 0.6, ancho_imagen * 0.4])
    fila_pie.setStyle(TableStyle([
        ("ALIGN", (0, 0), (0, 0), "LEFT"),
        ("ALIGN", (1, 0), (1, 0), "RIGHT"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 2 * mm),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
    ]))

    if es_importante:
        color_borde, grosor_borde = COLOR_ACENTO, 1.3
    elif es_cierre:
        color_borde, grosor_borde = COLOR_PRIMARIO, 1.3
    else:
        color_borde, grosor_borde = COLOR_BORDE, 0.5

    filas_tarjeta = [[contenido_imagen], [fila_pie]]

    # Renglones para notas manuscritas: solo en NORMAL e IMPORTANTE.
    # FIN_DE_TEMA queda sin renglones (funciona como cierre, no como contenido a desarrollar).
    if not es_cierre:
        estilo_notas_titulo = ParagraphStyle(
            "NotasTitulo", parent=estilos["Normal"], fontName=FUENTE_TITULO,
            fontSize=8, textColor=COLOR_TEXTO_SECUNDARIO, spaceBefore=3*mm, spaceAfter=1.5*mm,
        )
        titulo_notas = Table(
            [[Paragraph("NOTAS DEL DOCENTE", estilo_notas_titulo)]],
            colWidths=[ancho_imagen]
        )
        titulo_notas.setStyle(TableStyle([
            ("TOPPADDING", (0,0), (-1,-1), 0), ("BOTTOMPADDING", (0,0), (-1,-1), 0),
            ("LEFTPADDING", (0,0), (-1,-1), 0), ("RIGHTPADDING", (0,0), (-1,-1), 0),
        ]))
        filas_tarjeta.append([titulo_notas])

        lineas = []
        for _ in range(3):
            fila_linea = Table([[""]], colWidths=[ancho_imagen], rowHeights=[7*mm])
            fila_linea.setStyle(TableStyle([
                ("LINEBELOW", (0,0), (0,0), 0.6, COLOR_RENGLON),
                ("TOPPADDING", (0,0), (-1,-1), 0), ("BOTTOMPADDING", (0,0), (-1,-1), 0),
            ]))
            lineas.append([fila_linea])

        bloque_renglones = Table(lineas, colWidths=[ancho_imagen])
        bloque_renglones.setStyle(TableStyle([
            ("TOPPADDING", (0,0), (-1,-1), 0), ("BOTTOMPADDING", (0,0), (-1,-1), 0),
            ("LEFTPADDING", (0,0), (-1,-1), 0), ("RIGHTPADDING", (0,0), (-1,-1), 0),
        ]))
        filas_tarjeta.append([bloque_renglones])

    tarjeta = Table(filas_tarjeta, colWidths=[ancho_imagen])
    tarjeta.setStyle(TableStyle([
        ("BOX", (0, 0), (0, 0), grosor_borde, color_borde),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
    ]))

    return KeepTogether(tarjeta)

def _validar_temas_pdf(temas):
    numeros_vistos = set()
    for posicion, tema in enumerate(temas, start=1):
        if tema.get("numero_tema") != posicion:
            raise ValueError("Los temas deben estar numerados consecutivamente desde 1.")
        capturas_tema = tema.get("capturas")
        if not isinstance(capturas_tema, list) or not capturas_tema:
            raise ValueError(f"El tema {posicion} debe contener al menos una captura.")

        for indice, captura in enumerate(capturas_tema):
            numero_captura = captura.get("numero_captura")
            if numero_captura in numeros_vistos:
                raise ValueError(f"numero_captura duplicado en PDF: {numero_captura}")
            numeros_vistos.add(numero_captura)
            tipo_evento = captura.get("tipo_evento")
            if tipo_evento not in CATEGORIA_POR_EVENTO:
                raise ValueError(f"tipo_evento no soportado por RF16: {tipo_evento!r}")
            if captura.get("categoria") != CATEGORIA_POR_EVENTO[tipo_evento]:
                raise ValueError(f"Categoría incoherente en captura {numero_captura}.")
            if tipo_evento == "FIN_DE_TEMA" and indice != len(capturas_tema) - 1:
                raise ValueError("FIN_DE_TEMA debe ser la última captura de su tema.")

        termina_en_cierre = capturas_tema[-1]["tipo_evento"] == "FIN_DE_TEMA"
        if bool(tema.get("cerrado")) != termina_en_cierre:
            raise ValueError(f"Estado de cierre incoherente en tema {posicion}.")


def _crear_bloque_tema(tema, ancho_util):
    """Conecta la composición original de Daniela con la lista ordenada de RF14."""
    elementos = [Paragraph(f"TEMA {tema['numero_tema']}", estilo_titulo_tema)]
    for captura in tema["capturas"]:
        elementos.append(crear_tarjeta_captura(captura, ancho_util))
        if captura["tipo_evento"] != "FIN_DE_TEMA":
            elementos.append(Spacer(1, 8 * mm))
    if not tema["cerrado"]:
        elementos.append(Paragraph("Tema abierto - no se registró FIN DE TEMA.", estilo_metadato))
    return elementos


def generar_pdf_clase(temas, salida_pdf, datos_clase=None):
    """RF16: genera el PDF robusto con la identidad visual original de Daniela."""
    temas = list(temas)
    _validar_temas_pdf(temas)

    if datos_clase is None:
        datos_clase = {}
    elif not isinstance(datos_clase, dict):
        raise ValueError("datos_clase debe ser un dict o None.")
    else:
        datos_clase = dict(datos_clase)

    datos_portada = dict(DATOS_PORTADA_DANIELA)
    datos_portada.update(datos_clase)
    salida_pdf = Path(salida_pdf).expanduser()
    if salida_pdf.suffix.lower() != ".pdf":
        raise ValueError("salida_pdf debe tener extensión .pdf.")
    salida_pdf.parent.mkdir(parents=True, exist_ok=True)

    margen = 20 * mm
    documento = SimpleDocTemplate(
        str(salida_pdf), pagesize=A4, topMargin=28 * mm, bottomMargin=20 * mm,
        leftMargin=margen, rightMargin=margen,
        title=str(datos_portada.get("titulo_clase") or "Pizarra Snap"), author="Pizarra Snap",
    )
    ancho_util = A4[0] - 2 * margen

    # --- Armo el contenido (story) ---
    # La portada se dibuja directo sobre el canvas (onFirstPage).
    # Este PageBreak asegura que el contenido de los temas arranque
    # en la página 2, sin superponerse con la portada.
    story = [PageBreak()]
    for tema in temas:
        story.extend(_crear_bloque_tema(tema, ancho_util))

    try:
        with tempfile.TemporaryDirectory(prefix="fondos_", dir=salida_pdf.parent) as fondos_dir:
            fondo_portada, fondo_contenido = _crear_fondos_marca_temporales(fondos_dir)
            # --- Preparo las funciones de portada y encabezado con sus datos fijos ---
            portada_configurada = partial(
                dibujar_portada,
                fecha_clase=datos_portada.get("fecha_clase"),
                titulo_clase=datos_portada.get("titulo_clase"),
                institucion=datos_portada.get("institucion"),
                docente=datos_portada.get("docente"),
                materia=datos_portada.get("materia"),
                curso=datos_portada.get("curso"),
                unidad_tematica=datos_portada.get("unidad_tematica"),
                clase_numero=datos_portada.get("clase_numero"),
                fondo_portada_path=fondo_portada,
            )
            contenido_configurado = partial(encabezado_pie_pagina, fondo_contenido_path=fondo_contenido)
            # --- Construyo el documento ---
            documento.build(story, onFirstPage=portada_configurada, onLaterPages=contenido_configurado)
    except Exception as exc:
        raise RuntimeError(f"No se pudo generar el PDF en {salida_pdf}: {exc}") from exc

    if not salida_pdf.is_file():
        raise IOError(f"El PDF no fue creado: {salida_pdf}")
    if salida_pdf.stat().st_size <= 0:
        raise IOError(f"El PDF quedó vacío: {salida_pdf}")
    return salida_pdf.resolve()


def procesar_video(
    ruta_video: str | Path,
    directorio_trabajo: str | Path,
) -> tuple[Path, dict]:
    """Procesa un MP4 y devuelve (ruta del PDF, resumen sin imágenes).

    Conserva únicamente el PDF en el directorio de trabajo. El nombre es
    distinto para cada ejecución, incluso si se reutiliza ese directorio.
    """
    ruta_video = Path(ruta_video).expanduser().resolve(strict=True)
    if not ruta_video.is_file() or ruta_video.suffix.lower() != ".mp4":
        raise ValueError("La entrada debe ser un archivo MP4.")

    trabajo = Path(directorio_trabajo).expanduser().resolve()
    trabajo.mkdir(parents=True, exist_ok=True)

    video = cv2.VideoCapture(str(ruta_video))
    try:
        if not video.isOpened():
            raise ValueError("OpenCV no pudo abrir el MP4.")
        fps = video.get(cv2.CAP_PROP_FPS)
        total_frames = video.get(cv2.CAP_PROP_FRAME_COUNT)
        if not math.isfinite(fps) or fps <= 0:
            raise ValueError("El MP4 no informa una tasa de frames válida.")
        if not math.isfinite(total_frames) or total_frames < 1:
            raise ValueError("El MP4 no informa una cantidad de frames válida.")
        capturas = _detectar_capturas(video, fps, int(total_frames))
    finally:
        video.release()

    with tempfile.TemporaryDirectory(prefix="pizarra_snap_", dir=trabajo) as temporal:
        temporal = Path(temporal)
        cantidad_candidatos = [len(captura["frames_candidatos"]) for captura in capturas]
        resultados_walter = procesar_capturas(capturas, temporal / "capturas")
        resultados_reporte = adaptar_para_reporte(resultados_walter)
        temas = agrupar_por_temas(resultados_reporte)
        pdf_temporal = generar_pdf_clase(temas, temporal / "reporte.pdf")
        with pdf_temporal.open("rb") as archivo_pdf:
            paginas = len(PdfReader(archivo_pdf).pages)

        resumen = {
            "total_capturas": len(resultados_reporte),
            "total_temas": len(temas),
            "paginas_pdf": paginas,
            "capturas": [
                {
                    "tipo_evento": resultado["tipo_evento"],
                    "momento_del_evento": resultado["momento_del_evento"],
                    "cantidad_candidatos": cantidad,
                    "indice_mejor_frame": resultado["indice_mejor_frame"],
                    "metricas_mejor_frame": resultado["metricas_mejor_frame"],
                    "fuente_imagen": registro["fuente_imagen"],
                }
                for resultado, cantidad, registro in zip(
                    resultados_walter, cantidad_candidatos, resultados_reporte, strict=True
                )
            ],
            "temas": [
                {
                    "numero_tema": tema["numero_tema"],
                    "cantidad_capturas": len(tema["capturas"]),
                    "cerrado": tema["cerrado"],
                }
                for tema in temas
            ],
        }
        pdf = pdf_temporal.replace(temporal.with_suffix(".pdf"))
    return pdf, resumen
