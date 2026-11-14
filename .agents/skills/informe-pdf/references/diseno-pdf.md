# Diseño del PDF de Pizarra Snap

La identidad visual original de Daniela se implementa en [pipeline.py](../../../../pipeline.py).

| Elemento | Implementación |
|---|---|
| Página | A4. `generar_pdf_clase()` usa márgenes de 20 mm a los lados y abajo y 28 mm arriba. |
| Paleta | `COLOR_FONDO` declara `#FAFAFA`, el color base de los fondos. Primario `#157A6E`, acento `#F5A623`, texto `#1A1A1A`, secundario `#6B7280`, bordes `#E5E7EB` y renglones `#B8C4C2`. |
| Tipografía | `FUENTE_TITULO`, `FUENTE_TAGLINE` y `FUENTE_TEXTO` usan Helvetica-Bold, Helvetica-Oblique y Helvetica. |
| Fondos y marca | `_crear_fondos_marca_temporales()` prepara fondos distintos para portada y contenido con Pillow. `dibujar_simbolo()` y `dibujar_wordmark()` componen la marca. |
| Portada | `dibujar_portada()` incluye marca, título y ficha. `DATOS_PORTADA_DANIELA` contiene datos de ejemplo, entre ellos UTN y DIPLOMATURA EN IA. `datos_clase` permite sustituirlos en el generador. La fecha usa el día de ejecución cuando falta `fecha_clase`. |
| Encabezado y pie | `encabezado_pie_pagina()` dibuja el encabezado de marca, un separador y el número de página en el pie. Se aplica a las páginas posteriores a la portada. |
| Imágenes | `_imagen_para_pdf()` ajusta la imagen al espacio disponible manteniendo la proporción. El alto máximo predeterminado es 96 mm. Usa un marcador si la imagen falta o no puede abrirse. |
| Tarjetas | `crear_tarjeta_captura()` muestra categoría y momento. Usa borde gris para NORMAL, ámbar para IMPORTANTE y verde para FIN_DE_TEMA. |
| Notas | NORMAL e IMPORTANTE incluyen «NOTAS DEL DOCENTE» y tres renglones continuos mediante `LINEBELOW`. FIN_DE_TEMA cierra el bloque sin renglones. |
| Temas | `_crear_bloque_tema()` usa el título numerado y las tarjetas en orden. Indica si el tema quedó abierto. El contenido comienza después de la portada. |

Para comparar una modificación visual, fijá los datos de portada y la fecha, usá las mismas imágenes y renderizá ambas versiones con el mismo entorno. Revisá las tres categorías y la paginación.
