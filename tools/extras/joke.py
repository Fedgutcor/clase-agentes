"""
Tool: joke
Uso en el bot: "cuéntame un chiste" o "chiste"
Usa jokeapi.dev (sin API key).
"""
import urllib.request
import json

def get_joke(lang: str = "es") -> str:
    try:
        url = "https://v2.jokeapi.dev/joke/Any?blacklistFlags=nsfw,racist,sexist&lang=es&type=twopart"
        with urllib.request.urlopen(url, timeout=5) as r:
            data = json.loads(r.read())
        if data.get("type") == "twopart":
            return f"😄 {data['setup']}\n\n...{data['delivery']}"
        return f"😄 {data.get('joke', 'No encontré chistes.')}"
    except Exception as e:
        return f"No pude traer un chiste: {e}"
