import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
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

load_dotenv()

_console = Console()

logging.basicConfig(
    level=logging.WARNING,
    format="%(message)s",
    handlers=[RichHandler(console=_console, show_path=False, rich_tracebacks=True)],
)
log = logging.getLogger("bot")

# ── Clientes IA ───────────────────────────────────────────────────────────────

gemini      = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ── Prompts ───────────────────────────────────────────────────────────────────

SYSTEM = open("prompts/system.txt").read() + "\n" + open("prompts/personality.txt").read()

# ── Router ────────────────────────────────────────────────────────────────────

def choose_model(message: str) -> str:
    if any(w in message.lower() for w in ["rápido", "rapido", "corto", "simple"]):
        return "groq"
    return "gemini"

# ── IA ────────────────────────────────────────────────────────────────────────

def ask_ai(model: str, user_context: str, message: str) -> str:
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
        log.warning(f"Gemini falló ({e}) — usando Groq como fallback")
        response = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
        )
        return f"[fallback groq] {response.choices[0].message.content}"

# ── Handler ───────────────────────────────────────────────────────────────────

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id   = str(update.effective_user.id)
    username  = update.effective_user.first_name or user_id
    message   = update.message.text

    _console.print(
        f"  [dim cyan]▸[/dim cyan] [bold]{username}[/bold] [dim]({user_id})[/dim]  "
        f"[white]{message}[/white]"
    )

    if message.lower().startswith("calcula "):
        reply = calculate(message[8:])
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

    user_context = mem.get_context(user_id)
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

def _print_banner():
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
    _console.print(Padding("[bold cyan]Escuchando mensajes...[/bold cyan]", (0, 0, 1, 2)))

# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import asyncio
    asyncio.set_event_loop(asyncio.new_event_loop())
    token = os.getenv("TELEGRAM_TOKEN")
    app   = ApplicationBuilder().token(token).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    _print_banner()
    app.run_polling()
