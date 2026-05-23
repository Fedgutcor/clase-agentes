"""
Tool: reminder
Uso en el bot: "recuérdame en 10 minutos: llamar al médico"
Nota: los recordatorios se pierden si reinicias el bot (no hay persistencia en esta versión simple).
"""
import threading
import asyncio

_pending: list[dict] = []  # lista de recordatorios activos (en memoria, no en disco)

def set_reminder(delay_minutes: float, message: str, callback) -> str:
    """
    Programa un recordatorio para dentro de `delay_minutes` minutos.

    callback: función async que recibe el mensaje cuando se cumple el tiempo.
    En app.py úsalo así:

        async def send_reminder(msg):
            await update.message.reply_text(f"⏰ Recordatorio: {msg}")
        set_reminder(10, "llamar al médico", send_reminder)
    """
    def _fire():
        # threading.Timer no puede ejecutar código async directamente,
        # así que creamos un nuevo event loop solo para este momento
        loop = asyncio.new_event_loop()
        loop.run_until_complete(callback(message))
        loop.close()

    # Timer inicia un hilo en segundo plano que espera `delay_minutes * 60` segundos
    t = threading.Timer(delay_minutes * 60, _fire)
    t.daemon = True  # si el bot se cierra, el timer se cancela automáticamente
    t.start()
    _pending.append({"message": message, "minutes": delay_minutes, "timer": t})

    mins = int(delay_minutes)
    secs = int((delay_minutes - mins) * 60)
    if mins > 0:
        return f"⏰ Te recuerdo en {mins} min{f' {secs}s' if secs else ''}: {message}"
    return f"⏰ Te recuerdo en {secs} segundos: {message}"
