import sys
import os

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.live import Live
from rich.spinner import Spinner
from rich.text import Text
from rich import box

console = Console()

STANDALONE = __name__ == "__main__"

BANNER = """\
 ██████╗ ██╗      █████╗ ███████╗███████╗
██╔════╝ ██║     ██╔══██╗██╔════╝██╔════╝
██║      ██║     ███████║███████╗█████╗
██║      ██║     ██╔══██║╚════██║██╔══╝
╚██████╗ ███████╗██║  ██║███████║███████╗
 ╚═════╝ ╚══════╝╚═╝  ╚═╝╚══════╝╚══════╝

     CONSTRUYE TU PRIMER AGENTE IA
       Telegram · Gemini · Groq\
"""

if STANDALONE:
    console.print(Panel(BANNER, border_style="cyan", box=box.DOUBLE, padding=(1, 4)))
    console.print()


# ── Checks ────────────────────────────────────────────────────────────────────

def assert_python():
    assert sys.version_info >= (3, 10), (
        f"Python {sys.version_info.major}.{sys.version_info.minor} — necesitas 3.10+"
    )

def require_env(key):
    val = os.getenv(key)
    if not val or val.startswith("tu_"):
        raise Exception(f"no configurada")

CHECKS = [
    ("Python >= 3.10",        assert_python,
     "Descarga Python 3.10+ en python.org"),
    ("python-telegram-bot",   lambda: __import__("telegram"),
     "pip install python-telegram-bot==21.9"),
    ("google-genai",          lambda: __import__("google.genai"),
     "pip install google-genai"),
    ("groq",                  lambda: __import__("groq"),
     "pip install groq"),
    ("python-dotenv",         lambda: __import__("dotenv"),
     "pip install python-dotenv"),
    (".env existe",           lambda: open(".env").close(),
     "cp .env.example .env  →  luego llena tus keys"),
]

results = []
errors  = []

console.print("  [bold]Verificando entorno...[/bold]")
console.print()

for label, fn, fix in CHECKS:
    with Live(
        Text(f"  [dim]  ◌  {label}[/dim]"),
        console=console,
        refresh_per_second=12,
        transient=True,
    ):
        try:
            fn()
            results.append(("ok", label, None, None))
        except Exception as e:
            results.append(("fail", label, str(e), fix))
            errors.append((label, str(e), fix))

    if results[-1][0] == "ok":
        console.print(f"  [bold green]✓[/bold green]  {label}")
    else:
        console.print(f"  [bold red]✗[/bold red]  {label}  [dim red]— {results[-1][2]}[/dim red]")

# Cargar .env antes de verificar keys
from dotenv import load_dotenv
load_dotenv()

KEY_CHECKS = [
    ("TELEGRAM_TOKEN", "@BotFather en Telegram → /newbot → copiá el token"),
    ("GEMINI_API_KEY", "aistudio.google.com → Get API key"),
    ("GROQ_API_KEY",   "console.groq.com → API Keys → Create"),
]

console.print()
console.print("  [bold]Verificando API keys...[/bold]")
console.print()

for key, fix in KEY_CHECKS:
    with Live(
        Text(f"  [dim]  ◌  {key}[/dim]"),
        console=console,
        refresh_per_second=12,
        transient=True,
    ):
        try:
            require_env(key)
            results.append(("ok", key, None, None))
        except Exception as e:
            results.append(("fail", key, str(e), fix))
            errors.append((key, str(e), fix))

    if results[-1][0] == "ok":
        console.print(f"  [bold green]✓[/bold green]  {key}")
    else:
        console.print(f"  [bold red]✗[/bold red]  {key}  [dim red]— {results[-1][2]}[/dim red]")

console.print()


# ── Conclusión ────────────────────────────────────────────────────────────────

if not errors:
    console.print(Panel(
        "[bold green]Todo en orden.[/bold green]\n\n"
        "Arrancá el bot con:\n\n"
        "  [bold cyan]python app.py[/bold cyan]",
        border_style="green",
        box=box.ROUNDED,
        padding=(1, 4),
    ))
    if not STANDALONE:
        sys.exit(0)
else:
    lines = Text()
    lines.append("Hay errores que resolver antes de continuar.\n\n", style="bold red")
    for label, msg, fix in errors:
        lines.append(f"  ✗  {label}\n", style="red")
        if fix:
            lines.append(f"     → {fix}\n\n", style="dim")
    console.print(Panel(lines, border_style="red", box=box.ROUNDED, padding=(1, 3)))
    if not STANDALONE:
        sys.exit(1)

console.print()
