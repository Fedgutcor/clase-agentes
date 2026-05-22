"""
Tool: translator
Uso en el bot: "traduce al inglés: hola mundo" o "traduce al francés: buenos días"
Requiere: GROQ_API_KEY (ya la tienes configurada)
"""
import os
from groq import Groq

_client = None

def _get_client():
    global _client
    if _client is None:
        _client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    return _client

LANGUAGES = {
    "inglés": "English", "ingles": "English",
    "francés": "French", "frances": "French",
    "portugués": "Portuguese", "portugues": "Portuguese",
    "alemán": "German", "aleman": "German",
    "italiano": "Italian",
    "japonés": "Japanese", "japones": "Japanese",
}

def translate(target_lang: str, text: str) -> str:
    lang = LANGUAGES.get(target_lang.lower(), target_lang)
    try:
        response = _get_client().chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{
                "role": "user",
                "content": f"Translate the following text to {lang}. Return ONLY the translation, no explanations:\n\n{text}"
            }]
        )
        return f"({lang}): {response.choices[0].message.content.strip()}"
    except Exception as e:
        return f"No pude traducir: {e}"
