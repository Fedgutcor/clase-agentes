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
    Telegram · Gemini · Groq · NVIDIA\
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
    ("openai",                lambda: __import__("openai"),
     "pip install openai"),
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
    ("TELEGRAM_TOKEN", "@BotFather en Telegram → /newbot → copia el token"),
    ("GEMINI_API_KEY", "aistudio.google.com → Get API key"),
    ("GROQ_API_KEY",   "console.groq.com → API Keys → Create"),
    ("NVIDIA_API_KEY", "build.nvidia.com → elige un modelo → Get API Key"),
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


# ── Modelos ───────────────────────────────────────────────────────────────────
# Que la key exista no garantiza que el modelo responda: los proveedores retiran
# modelos cada pocos meses y la API empieza a contestar 404 ("not found") o 410
# ("gone"). Por eso le hacemos una pregunta real y muy corta a cada modelo.

def status_of(e):
    """Saca el código HTTP de un error, venga de la librería que venga."""
    for attr in ("status_code", "code"):
        value = getattr(e, attr, None)
        if isinstance(value, int):
            return value
    return None

def ask_model(provider, model):
    prompt = "Responde solo con la palabra: listo"
    if provider == "gemini":
        from google import genai
        client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        text = client.models.generate_content(model=model, contents=prompt).text
    else:
        if provider == "groq":
            from groq import Groq
            client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        else:
            from openai import OpenAI
            client = OpenAI(api_key=os.getenv("NVIDIA_API_KEY"),
                            base_url="https://integrate.api.nvidia.com/v1")
        response = client.chat.completions.create(
            model=model, messages=[{"role": "user", "content": prompt}],
        )
        text = response.choices[0].message.content
    if not text or not text.strip():
        raise Exception("el modelo respondió vacío")

failed_keys = {label for label, _, _ in errors}

try:
    from models import GEMINI_MODEL, GROQ_MODEL, NVIDIA_MODEL
    MODEL_CHECKS = [
        ("gemini", GEMINI_MODEL, "GEMINI_API_KEY", "GEMINI_MODEL", "aistudio.google.com"),
        ("groq",   GROQ_MODEL,   "GROQ_API_KEY",   "GROQ_MODEL",   "console.groq.com/docs/models"),
        ("nvidia", NVIDIA_MODEL, "NVIDIA_API_KEY", "NVIDIA_MODEL", "build.nvidia.com"),
    ]
except Exception:
    MODEL_CHECKS = []  # si falta una librería, el error ya aparece arriba

if MODEL_CHECKS:
    console.print("  [bold]Probando los modelos con una pregunta real...[/bold]")
    console.print()

for provider, model, key, env_var, catalog in MODEL_CHECKS:
    label = f"{provider}: {model}"
    if key in failed_keys:
        console.print(f"  [dim]–  {label}  — se salta: falta {key}[/dim]")
        continue

    with Live(
        Text(f"  [dim]  ◌  {label}[/dim]"),
        console=console,
        refresh_per_second=12,
        transient=True,
    ):
        try:
            ask_model(provider, model)
            outcome = ("ok", None, None)
        except Exception as e:
            status = status_of(e)
            if status in (404, 410):
                outcome = ("fail", "el modelo ya no existe (lo retiraron)",
                           f"Elige otro en {catalog} y agrega a tu .env:  {env_var}=nombre-del-modelo")
            elif status in (401, 403):
                outcome = ("fail", "la key no es válida",
                           f"Revisa {key} en tu .env (sin espacios ni comillas)")
            elif status == 429:
                outcome = ("warn", "cuota por minuto agotada — el modelo existe", None)
            else:
                outcome = ("fail", str(e)[:120], f"Revisa {key} y {env_var} en tu .env")

    kind, msg, fix = outcome
    if kind == "ok":
        console.print(f"  [bold green]✓[/bold green]  {label}")
    elif kind == "warn":
        console.print(f"  [bold yellow]![/bold yellow]  {label}  [dim yellow]— {msg}[/dim yellow]")
    else:
        console.print(f"  [bold red]✗[/bold red]  {label}  [dim red]— {msg}[/dim red]")
        errors.append((label, msg, fix))

console.print()


# ── Conclusión ────────────────────────────────────────────────────────────────

if not errors:
    console.print(Panel(
        "[bold green]Todo en orden.[/bold green]\n\n"
        "Arranca el bot con:\n\n"
        "  [bold cyan]python app.py[/bold cyan]",
        border_style="green",
        box=box.ROUNDED,
        padding=(1, 4),
    ))
else:
    lines = Text()
    lines.append("Hay errores que resolver antes de continuar.\n\n", style="bold red")
    for label, msg, fix in errors:
        lines.append(f"  ✗  {label}\n", style="red")
        if fix:
            lines.append(f"     → {fix}\n\n", style="dim")
    console.print(Panel(lines, border_style="red", box=box.ROUNDED, padding=(1, 3)))

console.print()

# El código de salida le avisa a setup.py si todo salió bien (0) o no (1).
sys.exit(1 if errors else 0)
