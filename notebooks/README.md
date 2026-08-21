# Manual operativo del notebook

Esta carpeta contiene el notebook canónico de Pizarra Snap:

- [`PizarraSnap.ipynb`](PizarraSnap.ipynb)

El documento describe cómo ejecutar la versión actual sin modificar su código, metadata ni outputs.

## 1. Entorno soportado

El notebook está diseñado actualmente para **Google Colab**. Utiliza `google.colab.files` para cargar el video y descargar el PDF; por eso un Jupyter local no reproduce directamente el mismo flujo sin adaptaciones.

Requisitos operativos:

- una cuenta con acceso a Google Colab;
- conexión a Internet para abrir el notebook e instalar dependencias;
- acceso al video oficial;
- espacio y memoria suficientes durante la sesión.

No se garantiza un tiempo exacto de ejecución. El tiempo depende del runtime de Colab, los recursos asignados y el archivo procesado.

## 2. Obtener el notebook

1. Abrir el repositorio `nicodf91/pizarra-snap` en GitHub.
2. Confirmar que la rama seleccionada sea `main`.
3. Abrir [`notebooks/PizarraSnap.ipynb`](PizarraSnap.ipynb).
4. Descargar el archivo o abrirlo en Google Colab.

El notebook de `main` es la fuente de verdad funcional del proyecto.

## 3. Obtener el video oficial

El archivo utilizado para la validación final es:

```text
proyecto_pizzarasnap.mp4
```

Puede obtenerse desde el [enlace de Google Drive documentado por el proyecto](https://drive.google.com/file/d/1Vcixn88RZXEH3cLLovZQJBfYXKoIKlMb/view?usp=drive_link).

El video no está versionado en Git por su tamaño. Si el enlace no permite descargarlo, debe solicitarse acceso al equipo antes de ejecutar el notebook.

## 4. Ejecutar Run All

1. Abrir el notebook en Google Colab.
2. Seleccionar **Runtime → Run All**.
3. Esperar a que aparezca el selector de archivos.
4. Elegir exactamente `proyecto_pizzarasnap.mp4`.
5. No seleccionar archivos adicionales.
6. Mantener la sesión activa hasta que terminen RF01–RF16 y la descarga final.

## 5. Selector de archivos

El manejo actual del selector no es robusto si se cancela la carga o se eligen varios archivos. Ante cualquiera de esos casos, reiniciar la sesión y repetir Run All seleccionando un único video.

## 6. Mensajes esperados

Durante una ejecución correcta aparecen mensajes equivalentes a:

```text
Librerías cargadas correctamente.
Video cargado: proyecto_pizzarasnap.mp4
Video abierto correctamente.
Referencias calculadas.
Evento confirmado: CAPTURA_NORMAL
Ventana cerrada: CAPTURA_NORMAL
Evento confirmado: CONCEPTO_IMPORTANTE
Ventana cerrada: CONCEPTO_IMPORTANTE
Evento confirmado: FIN_DE_TEMA
Ventana cerrada: FIN_DE_TEMA
RF06-RF09 validado correctamente.
RF10, RF11, RF12 y RF15 validados con casos sintéticos.
RF14 validado: temas, cierres, orden, unicidad y no mutación.
Pipeline real validado.
```

Los segundos, scores, cantidad de candidatos, temas y páginas pueden variar con otro video. Los mensajes permiten comprobar por qué etapa avanza el pipeline, pero no reemplazan la lectura de un error si la ejecución se interrumpe.

## 7. Capturas generadas

En Google Colab, RF12 guarda las capturas de la sesión en:

```text
/content/capturas_pizarra_snap
```

Por cada evento se conserva una captura original PNG. RF15 puede generar además una versión procesada en escala de grises con CLAHE, pero sólo si mejora el contraste y conserva suficiente nitidez. La original nunca se reemplaza.

El almacenamiento de `/content` pertenece a la sesión de Colab. Los archivos pueden desaparecer cuando el runtime se reinicia o finaliza.

## 8. PDF final

RF16 recibe los temas de RF14, genera el documento y valida que exista, tenga contenido y pueda abrirse con `pypdf`.

En Colab, la ruta utilizada actualmente es:

```text
/tmp/pizarra_snap_reportes/reporte_pizarra_snap_real.pdf
```

`/tmp` es almacenamiento temporal y efímero. La ruta puede dejar de existir cuando finaliza la sesión.

El número de páginas depende de las capturas y temas. No es una constante del algoritmo.

## 9. Descarga automática

La última celda comprueba si existe `pdf_path_real`. Cuando existe y el entorno es Google Colab, ejecuta la descarga del PDF mediante `google.colab.files.download`.

La descarga está separada de `generar_pdf_clase`:

```text
RF16 genera y valida el archivo
        ↓
la última celda inicia la descarga en Colab
```

El navegador puede solicitar permiso para descargar el archivo.

## 10. Recuperación manual del PDF

Si el navegador bloquea la descarga automática:

1. Mantener activa la sesión de Colab.
2. Abrir el panel **Files** de Colab.
3. Navegar hasta `/tmp/pizarra_snap_reportes/`.
4. Descargar `reporte_pizarra_snap_real.pdf` manualmente.

Si la sesión ya terminó, el almacenamiento temporal puede haberse eliminado y será necesario ejecutar nuevamente el notebook.

## 11. Resultado de la corrida oficial validada

Con `proyecto_pizzarasnap.mp4`, la ejecución final validada produjo:

| Resultado | Valor observado |
|---|---:|
| Eventos | 3, en el orden esperado |
| Frames candidatos | 57 por evento |
| Capturas seleccionadas | 3 |
| Temas | 1 tema cerrado |
| PDF | 3 páginas |
| Descarga | Automática en Colab |

Estos valores documentan una corrida concreta. Otro video puede producir cantidades diferentes.

## 12. Dependencias

| Dependencia | Disponibilidad actual |
|---|---|
| Python 3 | Runtime del notebook |
| OpenCV | Provisto normalmente por Colab |
| NumPy | Provisto normalmente por Colab |
| Matplotlib | Provisto normalmente por Colab |
| `google.colab` | Integración propia de Colab |
| ReportLab | Instalado por el notebook |
| Pillow | Instalado por el notebook |
| pypdf | Instalado por el notebook |

Las versiones no están fijadas. Definir versiones reproducibles es una mejora futura y no forma parte de la actualización documental actual.

## 13. Problemas frecuentes

### No se seleccionó ningún archivo

El código espera al menos un archivo. Reiniciar la sesión y repetir Run All.

### Se seleccionaron varios archivos

El código toma el primer archivo devuelto por el selector. Para evitar ambigüedad, reiniciar y seleccionar únicamente el video oficial.

### OpenCV no puede abrir el video

Comprobar que el archivo sea el MP4 oficial, que la carga haya terminado y que el nombre mostrado sea el esperado.

### No aparece el PDF

Buscar el primer error anterior en la ejecución. La celda final sólo descarga el archivo si `pdf_path_real` fue creado correctamente.

### La descarga fue bloqueada

Permitir descargas para Colab o utilizar la recuperación manual mientras la sesión siga activa.

## Documentación relacionada

- [Presentación y onboarding general](../README.md)
- [Arquitectura, RF, contratos, decisiones e historia](../PLAN_TRABAJO_PIZARRA_SNAP.md)
