"""Envío por correo electrónico del PDF generado por Pizarra Snap."""

import re
import smtplib
from email.message import EmailMessage

SERVIDOR_SMTP = "smtp.gmail.com"
PUERTO_SMTP = 465  # Conexión cifrada (SSL).
PATRON_EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def email_valido(direccion):
    """Indica si el texto tiene forma de dirección de correo."""
    return bool(PATRON_EMAIL.match(direccion.strip()))


def leer_credenciales(secretos):
    """Devuelve (usuario, clave) desde los secretos, o None si no están.

    Cualquier problema al leerlos (archivo ausente, sección o campo faltante)
    se trata como "no configurado": la app sigue funcionando sin el envío.
    """
    try:
        seccion = secretos["email"]
        usuario = str(seccion["usuario"]).strip()
        clave = str(seccion["clave"]).replace(" ", "")
    except Exception:
        return None
    if not usuario or not clave:
        return None
    return usuario, clave


def armar_mensaje(usuario, destino, pdf, nombre_archivo):
    """Arma el correo con el PDF adjunto."""
    mensaje = EmailMessage()
    mensaje["Subject"] = "Tu reporte de Pizarra Snap"
    mensaje["From"] = usuario
    mensaje["To"] = destino.strip()
    mensaje.set_content(
        "Hola!\n\n"
        "Adjuntamos el reporte PDF generado con Pizarra Snap.\n\n"
        "Pizarra Snap"
    )
    mensaje.add_attachment(
        pdf,
        maintype="application",
        subtype="pdf",
        filename=nombre_archivo,
    )
    return mensaje


def enviar_pdf(destino, pdf, credenciales, nombre_archivo="reporte_pizarra_snap.pdf"):
    """Envía el PDF a `destino` usando la cuenta indicada en `credenciales`."""
    usuario, clave = credenciales
    mensaje = armar_mensaje(usuario, destino, pdf, nombre_archivo)
    with smtplib.SMTP_SSL(SERVIDOR_SMTP, PUERTO_SMTP, timeout=30) as servidor:
        servidor.login(usuario, clave)
        servidor.send_message(mensaje)
