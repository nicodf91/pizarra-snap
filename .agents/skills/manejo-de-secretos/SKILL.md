---
name: manejo-de-secretos
description: 'Revisar la configuración de Gmail y Streamlit para RF17, prevenir exposición de credenciales y probar el envío del PDF con datos ficticios.'
---

# Secretos de RF17

1. Consultá [app.py](../../../app.py), [email_sender.py](../../../email_sender.py), el [ejemplo versionado](../../../.streamlit/secrets.toml.example), [.gitignore](../../../.gitignore) y el [contrato de RF17](../../../docs/REQUERIMIENTOS.md#interfaz-web--rf17). Verificá el esquema mediante el ejemplo. Omití la lectura de archivos privados de secretos y el acceso a valores reales.
2. `leer_credenciales(st.secrets)` busca `[email]` con `usuario` y `clave`. Recorta el usuario y quita espacios de la clave. Devuelve `None` ante campos vacíos o errores de lectura. `mostrar_envio_por_email()` deshabilita el formulario cuando falta configuración. `enviar_pdf()` usa Gmail por SMTP SSL en el puerto 465, a solicitud del usuario y a partir del PDF de la sesión.
3. Comprobá la regla de Git con `git check-ignore --no-index -- .streamlit/secrets.toml` y que el archivo privado quede fuera del índice con `git ls-files -- .streamlit/secrets.toml`. Inspeccioná los cambios nuevos y preparados para commit sin mostrar posibles valores sensibles. Una regla de exclusión no protege un archivo ya rastreado ni limpia el historial.
4. Validá con diccionarios ficticios para configuración ausente, incompleta y válida. Simulá `smtplib.SMTP_SSL` para comprobar autenticación, destinatario y adjunto con datos ficticios. Confirmá que la descarga sigue disponible y que un fallo de transporte produce un mensaje de interfaz sin detalles técnicos. Revisá el registro de excepciones en la app para evitar que una futura modificación exponga claves, contenido del PDF o datos del destinatario de forma innecesaria.
5. Si sospechás una exposición, detené el commit o la publicación y avisá al responsable indicando ruta y alcance sin copiar el valor. Si se expuso una credencial real, su titular debe revocarla y reemplazarla. Coordiná el saneamiento de Git y logs con el equipo y tratá cualquier reescritura de historial como una operación aparte.

Las comprobaciones de esta skill se hacen sin enviar correos ni usar cuentas reales.
