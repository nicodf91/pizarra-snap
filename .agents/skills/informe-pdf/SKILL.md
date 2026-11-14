---
name: informe-pdf
description: 'Revisar o cambiar la clasificación RF13, los temas RF14, el diseño y la generación RF16 o el PDF adjunto de RF17 en Pizarra Snap.'
---

# Informe PDF

1. Identificá si el cambio afecta registros, agrupación, diseño o el adjunto. Localizá la función y su consumidor en el código vigente.
2. Leé [contratos](references/contratos.md) si cambia el paso de datos entre módulos, la elección de imágenes, la validación o el adjunto. Leé [diseño del PDF](references/diseno-pdf.md) si cambia la presentación. Abrí ambas referencias cuando el cambio afecte los dos aspectos.
3. Conservá la identidad de las capturas, el orden, el cierre de temas y la portada de referencia salvo que el pedido cambie ese comportamiento. En RF17, reutilizá el PDF de la sesión.
4. Probá según el alcance. Para contratos, usá capturas sintéticas normales, importantes y de cierre, un tema abierto y los casos de imagen ausente o ilegible. Para maquetación, usá `PdfReader` para verificar apertura, estructura y paginación del PDF; renderizá ambas versiones con el mismo motor, las mismas capturas y fecha fija para comparar visualmente portada, tarjetas y renglones. `PdfReader` por sí solo no verifica el estilo gráfico de los trazos. Para el adjunto, inspeccioná el mensaje con transporte simulado y compará los bytes con el PDF generado.
5. Si afecta el flujo completo, compará el resultado con el MP4 oficial y registrá el alcance de la comparación. En la base revisada la apertura del PDF se comprueba dentro de `procesar_video()`. Usá esos controles y los casos del notebook si están disponibles.

Las referencias se elaboraron a partir del código y del plan técnico. El borrador `SK_Informe_PDF.md` de Daniela no estuvo disponible durante esta revisión.
