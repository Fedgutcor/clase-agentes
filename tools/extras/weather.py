"""
Tool: weather
Uso en el bot: "clima en Medellín" o "tiempo en Buenos Aires"
"""
import urllib.request
import json

def get_weather(city: str) -> str:
    try:
        city_encoded = city.replace(" ", "+")  # las URLs no aceptan espacios
        url = f"https://wttr.in/{city_encoded}?format=j1"
        with urllib.request.urlopen(url, timeout=5) as r:
            data = json.loads(r.read())  # convierte el JSON de la respuesta a diccionario Python
        current = data["current_condition"][0]
        temp   = current["temp_C"]
        feels  = current["FeelsLikeC"]
        desc   = current["weatherDesc"][0]["value"]
        humidity = current["humidity"]
        return f"🌤 {city}: {desc}, {temp}°C (sensación {feels}°C), humedad {humidity}%"
    except Exception as e:
        return f"No pude obtener el clima de {city}: {e}"
