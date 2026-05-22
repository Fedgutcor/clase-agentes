"""
Tool: currency
Uso en el bot: "convierte 100 USD a EUR" o "convierte 50000 COP a USD"
Usa frankfurter.app (sin API key, datos del BCE).
"""
import urllib.request
import json

def convert_currency(amount: float, from_cur: str, to_cur: str) -> str:
    try:
        from_cur = from_cur.upper()
        to_cur = to_cur.upper()
        url = f"https://api.frankfurter.app/latest?amount={amount}&from={from_cur}&to={to_cur}"
        with urllib.request.urlopen(url, timeout=5) as r:
            data = json.loads(r.read())
        result = data["rates"].get(to_cur)
        if result is None:
            return f"Moneda no soportada: {to_cur}"
        return f"💱 {amount} {from_cur} = {result:.2f} {to_cur}"
    except Exception as e:
        return f"No pude convertir la moneda: {e}"
