"""
Tool: reminder
Uso en el bot: "recuérdame en 10 minutos: llamar al médico"

Los recordatorios ahora se guardan en disco (memory/users/{id}.json).
Si el bot se reinicia, los timers pendientes se reconstruyen automáticamente al arrancar.
"""
import threading
import asyncio
import time

import memory as mem

def set_reminder(user_id: str, delay_minutes: float, message: str, callback) -> str:
    """
    Programa un recordatorio para dentro de `delay_minutes` minutos.

    - Guarda el recordatorio en disco antes de arrancar el timer.
    - Al dispararse, elimina el recordatorio del disco y llama a callback.

    callback: función async que recibe el texto del recordatorio.
    En app.py úsalo así:

        async def send_reminder(msg):
            await update.message.reply_text(f"⏰ Recordatorio: {msg}")
        set_reminder(user_id, 10, "llamar al médico", send_reminder)
    """
    fires_at = time.time() + delay_minutes * 60  # momento exacto en que debe sonar

    # Guardamos ANTES de arrancar el timer — si el bot cae en este instante,
    # el recordatorio ya está en disco y se recupera al reiniciar.
    mem.save_reminder(user_id, message, fires_at)

    _schedule(user_id, message, fires_at, delay_minutes * 60, callback)

    mins = int(delay_minutes)
    secs = int((delay_minutes - mins) * 60)
    if mins > 0:
        return f"⏰ Te recuerdo en {mins} min{f' {secs}s' if secs else ''}: {message}"
    return f"⏰ Te recuerdo en {secs} segundos: {message}"

def _schedule(user_id: str, message: str, fires_at: float, delay_seconds: float, callback):
    """Crea el timer interno. Separado para poder llamarlo también desde restore_reminders."""
    def _fire():
        mem.delete_reminder(user_id, message, fires_at)  # limpia el disco
        loop = asyncio.new_event_loop()
        loop.run_until_complete(callback(message))
        loop.close()

    # threading.Timer no puede ejecutar código async directamente,
    # así que creamos un nuevo event loop solo para ese momento
    t = threading.Timer(delay_seconds, _fire)
    t.daemon = True  # si el bot se cierra, el timer se cancela
    t.start()

def restore_reminders(get_callback) -> int:
    """
    Al arrancar el bot, recupera los recordatorios guardados en disco y recrea sus timers.

    get_callback: función que recibe un user_id y devuelve el callback async para ese usuario.
    Devuelve cuántos recordatorios se restauraron (útil para el log de arranque).

    Ejemplo de uso en app.py:
        def get_callback(user_id):
            async def send(msg):
                await app.bot.send_message(chat_id=user_id, text=f"⏰ Recordatorio: {msg}")
            return send
        restore_reminders(get_callback)
    """
    pending   = mem.get_all_reminders()
    restored  = 0
    now       = time.time()

    for r in pending:
        user_id  = r["user_id"]
        message  = r["message"]
        fires_at = r["fires_at"]
        delay    = fires_at - now

        if delay <= 0:
            # El recordatorio venció mientras el bot estaba apagado.
            # Lo enviamos de inmediato con una nota de que llegó tarde.
            async def _send_late(msg=message, uid=user_id):
                await get_callback(uid)(f"{msg} (llegó tarde — el bot estaba apagado)")
            loop = asyncio.new_event_loop()
            loop.run_until_complete(_send_late())
            loop.close()
            mem.delete_reminder(user_id, message, fires_at)
        else:
            _schedule(user_id, message, fires_at, delay, get_callback(user_id))

        restored += 1

    return restored
