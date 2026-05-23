import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes
from google import genai
from google.genai import errors as genai_errors
from groq import Groq

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.logging import RichHandler
from rich.padding import Padding
from rich import box

import memory as mem
from tools.calculator import calculate
from tools.notes import save_note, list_notes
from tools.extras.reminder import set_reminder, restore_reminders

load_dotenv()  # carga las variables del archivo .env (tus API keys)

_console = Console()

logging.basicConfig(
    level=logging.WARNING,
    format="%(message)s",
    handlers=[RichHandler(console=_console, show_path=False, rich_tracebacks=True)],
)
log = logging.getLogger("bot")

# ── Clientes IA ───────────────────────────────────────────────────────────────
# Cada modelo de IA tiene su propio "cliente": un objeto que sabe cómo hablarle.
# Le pasamos la API key para que el servicio sepa que somos nosotros.

gemini      = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ── Prompts ───────────────────────────────────────────────────────────────────
# El "system prompt" es lo que le dice a la IA quién es y cómo debe comportarse.
# Lo guardamos en archivos .txt para poder editarlo sin tocar el código.

SYSTEM = open("prompts/system.txt").read() + "\n" + open("prompts/personality.txt").read()

# ── Router ────────────────────────────────────────────────────────────────────
# El router decide qué modelo usar según el mensaje.
# Si el usuario pide algo rápido/simple → Groq (más veloz).
# Para todo lo demás → Gemini (más capaz).

def choose_model(message: str) -> str:
    if any(w in message.lower() for w in ["rápido", "rapido", "corto", "simple"]):
        return "groq"
    return "gemini"

# ── IA ────────────────────────────────────────────────────────────────────────
# Esta función construye el prompt completo y llama al modelo elegido.
# Si Gemini falla, automáticamente intenta con Groq (fallback).

def ask_ai(model: str, user_context: str, message: str) -> str:
    # Armamos el prompt completo: personalidad + memoria del usuario + mensaje actual
    prompt = f"{SYSTEM}\n{user_context}\nUsuario: {message}"

    if model == "groq":
        response = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content

    try:
        response = gemini.models.generate_content(
            model="gemini-2.0-flash", contents=prompt
        )
        return response.text
    except (genai_errors.APIError, genai_errors.ServerError, genai_errors.ClientError) as e:
        # Gemini falló (cuota, red, etc.) → usamos Groq como respaldo
        log.warning(f"Gemini falló ({e}) — usando Groq como fallback")
        response = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
        )
        # El prefijo [fallback groq] avisa que no fue la respuesta principal
        return f"[fallback groq] {response.choices[0].message.content}"

# ── Comando /start ────────────────────────────────────────────────────────────
# Se ejecuta cuando alguien abre el bot por primera vez o escribe /start.
# Es la primera impresión — debe explicar qué puede hacer el bot.

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.effective_user.first_name or "ahí"
    await update.message.reply_text(
        f"Hola, {username} 👋\n\n"
        "Soy un agente de IA con memoria. Puedo:\n\n"
        "🧠 Recordar cosas sobre ti\n"
        "   → recuerda que estudio diseño\n\n"
        "🗒 Guardar y listar tus notas\n"
        "   → guarda nota comprar leche\n"
        "   → mis notas\n\n"
        "🔢 Hacer cuentas\n"
        "   → calcula 45 * 12\n\n"
        "⏰ Programar recordatorios\n"
        "   → recuérdame en 10 minutos: llamar al médico\n\n"
        "⚡ Responder rápido con Groq\n"
        "   → rápido qué es una API\n\n"
        "Para todo lo demás, escríbeme y te respondo con Gemini. 🤖"
    )
    _console.print(f"  [dim cyan]▸[/dim cyan] /start — {username}")

# ── Handler de mensajes ───────────────────────────────────────────────────────
# Esta función se ejecuta cada vez que el bot recibe un mensaje de texto.
# Es el corazón del agente: decide qué hacer con cada mensaje.

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id  = str(update.effective_user.id)   # ID único del usuario en Telegram
    username = update.effective_user.first_name or user_id
    message  = update.message.text

    _console.print(
        f"  [dim cyan]▸[/dim cyan] [bold]{username}[/bold] [dim]({user_id})[/dim]  "
        f"[white]{message}[/white]"
    )

    # Primero revisamos si el mensaje activa alguna tool.
    # Las tools responden directamente, sin pasar por la IA.

    if message.lower().startswith("calcula "):
        reply = calculate(message[8:])  # le pasamos todo lo que viene después de "calcula "
        _console.print(f"  [dim green]  ↳ calculadora[/dim green]")
        await update.message.reply_text(reply)
        return

    if message.lower().startswith("guarda nota "):
        reply = save_note(user_id, message[12:])
        _console.print(f"  [dim green]  ↳ nota guardada[/dim green]")
        await update.message.reply_text(reply)
        return

    if message.lower() == "mis notas":
        reply = list_notes(user_id)
        _console.print(f"  [dim green]  ↳ notas listadas[/dim green]")
        await update.message.reply_text(reply)
        return

    if message.lower().startswith("recuerda que "):
        fact = message[13:]
        mem.add_fact(user_id, fact)
        _console.print(f"  [dim green]  ↳ memoria guardada[/dim green]")
        await update.message.reply_text(f"Lo recuerdo: {fact}")
        return

    if message.lower().startswith("recuérdame en ") or message.lower().startswith("recuerdame en "):
        # Formato esperado: "recuérdame en 10 minutos: llamar al médico"
        try:
            rest    = message.split("en ", 1)[1]           # "10 minutos: llamar al médico"
            parts   = rest.split(":", 1)                   # ["10 minutos", " llamar al médico"]
            minutes = float(parts[0].strip().split()[0])   # 10
            text    = parts[1].strip()                     # "llamar al médico"

            async def send_reminder(msg):
                await context.bot.send_message(chat_id=user_id, text=f"⏰ Recordatorio: {msg}")

            reply = set_reminder(user_id, minutes, text, send_reminder)
            _console.print(f"  [dim green]  ↳ recordatorio en {minutes} min[/dim green]")
            await update.message.reply_text(reply)
        except (IndexError, ValueError):
            await update.message.reply_text(
                "No entendí el formato. Prueba así:\n"
                "recuérdame en 10 minutos: llamar al médico"
            )
        return

    # Si no era una tool, consultamos la memoria del usuario y llamamos a la IA.
    user_context = mem.get_context(user_id)  # hechos que el usuario guardó antes
    model        = choose_model(message)
    response     = ask_ai(model, user_context, message)

    model_color = "green" if model == "gemini" else "yellow"
    _console.print(
        f"  [dim {model_color}]  ↳ {model.upper()}[/dim {model_color}]  "
        f"[dim]{response[:80]}{'…' if len(response) > 80 else ''}[/dim]"
    )

    model_tag = f"[{model.upper()}] " if os.getenv("SHOW_MODEL") else ""
    await update.message.reply_text(f"{model_tag}{response}")

# ── Banner ────────────────────────────────────────────────────────────────────
# Solo visual: imprime el logo y el estado del router cuando arranca el bot.

def _print_banner(restored: int):
    banner = Text(justify="center")
    banner.append("\n")
    banner.append(" ██████╗  ██████╗ ████████╗\n", style="bold cyan")
    banner.append("██╔══██╗██╔═══██╗╚══██╔══╝\n", style="bold cyan")
    banner.append("██████╔╝██║   ██║   ██║\n",    style="bold cyan")
    banner.append("██╔══██╗██║   ██║   ██║\n",    style="bold cyan")
    banner.append("██████╔╝╚██████╔╝   ██║\n",    style="bold cyan")
    banner.append("╚═════╝  ╚═════╝    ╚═╝\n",   style="bold cyan")
    banner.append("\n")
    banner.append("  🤖  AGENTE IA — ONLINE\n",   style="bold white")
    banner.append("  Telegram · Gemini · Groq\n", style="dim")
    _console.print(Panel(banner, border_style="cyan", box=box.DOUBLE, padding=(0, 4)))

    router = Table(box=box.SIMPLE, show_header=False, padding=(0, 2))
    router.add_column(no_wrap=True)
    router.add_column()
    router.add_column(style="dim")
    router.add_row("├──", "[bold green]Gemini 2.0 Flash[/bold green]", "default")
    router.add_row("└──", "[bold yellow]Groq Llama 3.1[/bold yellow]", "rápido / fallback")

    _console.print()
    _console.print(Padding("[bold]Router activo[/bold]", (0, 0, 0, 2)))
    _console.print(Padding(router, (0, 0, 0, 2)))

    if restored:
        _console.print(Padding(
            f"[dim yellow]⏰ {restored} recordatorio(s) restaurado(s) del disco[/dim yellow]",
            (0, 0, 0, 2)
        ))

    _console.print(Padding("[bold cyan]Escuchando mensajes...[/bold cyan]", (0, 0, 1, 2)))

# ── Main ──────────────────────────────────────────────────────────────────────
# Punto de entrada: conecta el bot a Telegram y empieza a escuchar mensajes.

if __name__ == "__main__":
    import asyncio
    asyncio.set_event_loop(asyncio.new_event_loop())
    token = os.getenv("TELEGRAM_TOKEN")
    app   = ApplicationBuilder().token(token).build()

    # Registramos los handlers: /start para el onboarding, el resto para mensajes normales
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Reconstruimos los recordatorios que estaban pendientes antes del reinicio.
    # get_callback recibe el user_id y devuelve la función que envía el mensaje por Telegram.
    def get_callback(user_id):
        async def send(msg):
            await app.bot.send_message(chat_id=user_id, text=f"⏰ Recordatorio: {msg}")
        return send

    restored = restore_reminders(get_callback)
    _print_banner(restored)
    app.run_polling()  # el bot corre indefinidamente hasta que presionas Ctrl+C
