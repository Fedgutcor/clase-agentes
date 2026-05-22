import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import google.generativeai as genai
from groq import Groq
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich import box

_console = Console()

import memory as mem
from tools.calculator import calculate
from tools.notes import save_note, list_notes

load_dotenv()

logging.basicConfig(level=logging.INFO)

# --- Clientes IA ---
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
gemini = genai.GenerativeModel("gemini-2.0-flash")
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# --- Prompts ---
SYSTEM = open("prompts/system.txt").read()

# --- Router: decide qué modelo usar ---
def choose_model(message: str) -> str:
    if any(w in message.lower() for w in ["rápido", "rapido", "corto", "simple"]):
        return "groq"
    return "gemini"

# --- Llama al modelo elegido ---
def ask_ai(model: str, user_context: str, message: str) -> str:
    prompt = f"{SYSTEM}\n{user_context}\nUsuario: {message}"

    if model == "groq":
        response = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content

    # Intenta Gemini; si falla (quota, error de red, etc.) cae a Groq
    try:
        response = gemini.generate_content(prompt)
        return response.text
    except Exception as e:
        logging.warning(f"Gemini falló ({e}), usando Groq como fallback")
        response = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}]
        )
        return f"[fallback groq] {response.choices[0].message.content}"

# --- Handler principal ---
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    message = update.message.text

    # Herramientas manuales (versión ingenua — luego usaríamos tool calling)
    if message.lower().startswith("calcula "):
        expr = message[8:]
        await update.message.reply_text(calculate(expr))
        return

    if message.lower().startswith("guarda nota "):
        note = message[12:]
        await update.message.reply_text(save_note(user_id, note))
        return

    if message.lower() == "mis notas":
        await update.message.reply_text(list_notes(user_id))
        return

    if message.lower().startswith("recuerda que "):
        fact = message[13:]
        mem.add_fact(user_id, fact)
        await update.message.reply_text(f"Lo recuerdo: {fact}")
        return

    # Memoria del usuario
    user_context = mem.get_context(user_id)

    # Routing de modelo
    model = choose_model(message)

    # Respuesta
    response = ask_ai(model, user_context, message)
    model_tag = f"[{model.upper()}] " if os.getenv("SHOW_MODEL") else ""
    await update.message.reply_text(f"{model_tag}{response}")

# --- Main ---
def _print_banner():
    banner = Text()
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
    _console.print(Panel(banner, border_style="cyan", box=box.DOUBLE, padding=(0, 2)))

    _console.print()
    _console.print("  [bold]Router activo[/bold]")
    _console.print("  ├── [green]Gemini 2.0 Flash[/green]  [dim](default)[/dim]")
    _console.print("  └── [yellow]Groq Llama 3.1[/yellow]   [dim](rápido / fallback)[/dim]")
    _console.print()
    _console.print("  [bold cyan]Escuchando mensajes...[/bold cyan]")
    _console.print()


if __name__ == "__main__":
    import asyncio
    asyncio.set_event_loop(asyncio.new_event_loop())
    token = os.getenv("TELEGRAM_TOKEN")
    app = ApplicationBuilder().token(token).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    _print_banner()
    app.run_polling()
