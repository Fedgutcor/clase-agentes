"""
Tool: qr_generator
Uso en el bot: "genera qr: https://google.com"
No requiere librerías externas — usa el servicio público de qr-code-generator.
Devuelve un link directo a la imagen PNG del QR.
"""
import urllib.parse

def generate_qr(text: str) -> str:
    encoded = urllib.parse.quote(text)
    url = f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={encoded}"
    return f"📱 QR generado para: {text}\n{url}"
