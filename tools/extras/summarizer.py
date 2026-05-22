"""
Tool: summarizer
Uso en el bot: "resume: [texto largo aquí]"
Requiere: GROQ_API_KEY
"""
import os
from groq import Groq

_client = None

def _get_client():
    global _client
    if _client is None:
        _client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    return _client

def summarize(text: str) -> str:
    if len(text) < 100:
        return "El texto es muy corto para resumir."
    try:
        response = _get_client().chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{
                "role": "user",
                "content": f"Resume el siguiente texto en 3 puntos clave, en el mismo idioma del texto:\n\n{text}"
            }]
        )
        return f"📝 Resumen:\n{response.choices[0].message.content.strip()}"
    except Exception as e:
        return f"No pude resumir: {e}"
