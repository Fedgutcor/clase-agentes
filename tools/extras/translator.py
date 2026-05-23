"""
Tool: translator
Uso en el bot: "traduce al inglés: hola mundo" o "traduce al francés: buenos días"
Requiere: GROQ_API_KEY (ya la tienes configurada)
"""
import os
from groq import Groq

# El cliente se crea una sola vez y se reutiliza (_client empieza en None)
_client = None

def _get_client():
    global _client
    if _client is None:
        _client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    return _client

# Mapa de nombres en español → código de idioma para la IA
# Incluye versiones con y sin tilde para no depender de que el usuario las escriba
LANGUAGES = {
    "inglés": "English", "ingles": "English",
    "francés": "French", "frances": "French",
    "portugués": "Portuguese", "portugues": "Portuguese",
    "alemán": "German", "aleman": "German",
    "italiano": "Italian",
    "japonés": "Japanese", "japones": "Japanese",
}

def translate(target_lang: str, text: str) -> str:
    lang = LANGUAGES.get(target_lang.lower(), target_lang)  # si no está en el mapa, usa el texto tal cual
    try:
        response = _get_client().chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{
                "role": "user",
                # Le pedimos explícitamente que devuelva SOLO la traducción,
                # para que no agregue frases como "Aquí está tu traducción:"
                "content": f"Translate the following text to {lang}. Return ONLY the translation, no explanations:\n\n{text}"
            }]
        )
        return f"({lang}): {response.choices[0].message.content.strip()}"
    except Exception as e:
        return f"No pude traducir: {e}"
