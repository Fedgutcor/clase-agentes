import sys
import os
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich import box

console = Console()

BANNER = """
 ██████╗ ██╗      █████╗ ███████╗███████╗
██╔════╝ ██║     ██╔══██╗██╔════╝██╔════╝
██║      ██║     ███████║███████╗█████╗
██║      ██║     ██╔══██║╚════██║██╔══╝
╚██████╗ ███████╗██║  ██║███████║███████╗
 ╚═════╝ ╚══════╝╚═╝  ╚═╝╚══════╝╚══════╝

     CONSTRUYE TU PRIMER AGENTE IA
       Telegram · Gemini · Groq
"""

checks = []
errors = []

def check(label, fn, fix=None):
    try:
        fn()
        checks.append(("ok", label))
    except Exception as e:
        checks.append(("fail", label, str(e), fix))
        errors.append((label, str(e), fix))


def assert_python():
    assert sys.version_info >= (3, 10), f"Python {sys.version_info.major}.{sys.version_info.minor} — necesitas 3.10+"

def require_env(key):
    val = os.getenv(key)
    if not val or val.startswith("tu_"):
        raise Exception(f"{key} no está configurada")


# --- Banner ---
console.print(Panel(BANNER, border_style="cyan", box=box.DOUBLE))

# --- Checks ---
console.print()
console.print("  [bold]Verificando setup...[/bold]")
console.print()

check("Python >= 3.10",          assert_python,
      "Descarga Python 3.10+ desde python.org")
check("python-telegram-bot",     lambda: __import__("telegram"),
      "pip install python-telegram-bot==21.9")
check("google-generativeai",     lambda: __import__("google.generativeai"),
      "pip install google-generativeai==0.8.3")
check("groq",                    lambda: __import__("groq"),
      "pip install groq")
check("python-dotenv",           lambda: __import__("dotenv"),
      "pip install python-dotenv")
check(".env existe",             lambda: open(".env").close(),
      "cp .env.example .env  →  luego llena tus keys")

from dotenv import load_dotenv
load_dotenv()

check("TELEGRAM_TOKEN",          lambda: require_env("TELEGRAM_TOKEN"),
      "@BotFather en Telegram → /newbot → copia el token")
check("GEMINI_API_KEY",          lambda: require_env("GEMINI_API_KEY"),
      "aistudio.google.com → Get API key")
check("GROQ_API_KEY",            lambda: require_env("GROQ_API_KEY"),
      "console.groq.com → API Keys → Create")

# --- Resultados ---
console.print()
for item in checks:
    if item[0] == "ok":
        console.print(f"  [bold green]✓[/bold green]  {item[1]}")
    else:
        console.print(f"  [bold red]✗[/bold red]  {item[1]}  [dim red]({item[2]})[/dim red]")

console.print()

# --- Conclusión ---
if not errors:
    console.print(Panel(
        "[bold green]Todo listo.[/bold green]\n\nCorre el bot con:\n\n  [bold cyan]python app.py[/bold cyan]",
        border_style="green",
        box=box.ROUNDED,
        padding=(1, 4),
    ))
else:
    lines = ["[bold red]Hay errores que resolver:[/bold red]\n"]
    for label, msg, fix in errors:
        lines.append(f"[red]✗[/red] [bold]{label}[/bold]")
        if fix:
            lines.append(f"  [dim]→ {fix}[/dim]")
        lines.append("")
    console.print(Panel(
        "\n".join(lines),
        border_style="red",
        box=box.ROUNDED,
        padding=(1, 4),
    ))

console.print()
