"""
Tool: pomodoro
Uso en el bot: "pomodoro 25" o "pomodoro"
Inicia un temporizador Pomodoro y avisa cuando termina.
Igual que reminder.py, necesita un callback async para notificar al usuario.
"""
import threading
import asyncio

DEFAULT_MINUTES = 25

def start_pomodoro(callback, minutes: int = DEFAULT_MINUTES) -> str:
    """
    Inicia un temporizador de `minutes` minutos y llama a `callback` cuando termina.

    En app.py úsalo así:
        async def notify(msg):
            await update.message.reply_text(msg)
        start_pomodoro(notify, 25)
    """
    def _fire():
        # Misma técnica que reminder.py: nuevo event loop para poder usar async desde un hilo
        loop = asyncio.new_event_loop()
        loop.run_until_complete(callback(
            f"🍅 ¡Pomodoro de {minutes} minutos terminado! Tómate un descanso de 5 minutos."
        ))
        loop.close()

    t = threading.Timer(minutes * 60, _fire)
    t.daemon = True  # si el bot se cierra, el timer se cancela
    t.start()
    return f"🍅 Pomodoro iniciado: {minutes} minutos de foco. ¡Éxito!"
