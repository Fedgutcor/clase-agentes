"""
setup.py — instalación guiada para la clase
Corre con: python setup.py
"""
import os
import sys
import subprocess
import platform
import time

from rich.console import Console
from rich.panel import Panel
from rich.rule import Rule
from rich.table import Table
from rich.text import Text
from rich.padding import Padding
from rich.live import Live
from rich.spinner import Spinner
from rich import box

console = Console()

IS_WINDOWS = platform.system() == "Windows"
PYTHON     = sys.executable
VENV_DIR   = "venv"
VENV_PY    = os.path.join(VENV_DIR, "Scripts" if IS_WINDOWS else "bin", "python")
VENV_PIP   = os.path.join(VENV_DIR, "Scripts" if IS_WINDOWS else "bin", "pip")


# ── Helpers ───────────────────────────────────────────────────────────────────

def step(n: int, title: str):
    console.print()
    badge = f"[bold white on cyan]  {n}  [/bold white on cyan]"
    console.print(f" {badge} [bold]{title}[/bold]")
    console.print(Padding(Rule(style="cyan dim"), (0, 0, 1, 0)))

def info(text: str):
    console.print(Padding(text, (0, 0, 0, 4)))

def ok(text: str):
    console.print(Padding(f"[bold green]✓[/bold green]  {text}", (0, 0, 0, 4)))

def run_silent(cmd: list, label: str):
    with Live(
        Padding(Spinner("dots", text=f"[dim]{label}[/dim]"), (0, 0, 0, 4)),
        console=console,
        refresh_per_second=12,
    ):
        result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        console.print(Padding(f"[bold red]Error:[/bold red] {label}", (0, 0, 0, 4)))
        console.print(Padding(result.stderr, (0, 0, 0, 6)))
        sys.exit(1)


# ── Banner ────────────────────────────────────────────────────────────────────

BANNER = """\
 ██████╗ ██╗      █████╗ ███████╗███████╗
██╔════╝ ██║     ██╔══██╗██╔════╝██╔════╝
██║      ██║     ███████║███████╗█████╗
██║      ██║     ██╔══██║╚════██║██╔══╝
╚██████╗ ███████╗██║  ██║███████║███████╗
 ╚═════╝ ╚══════╝╚═╝  ╚═╝╚══════╝╚══════╝

     CONSTRUYE TU PRIMER AGENTE IA
       Setup guiado · python setup.py\
"""

console.print()
console.print(Panel(BANNER, border_style="cyan", box=box.DOUBLE, padding=(1, 4)))
console.print()

intro = Table.grid(padding=(0, 2))
intro.add_column(style="cyan bold")
intro.add_column()
intro.add_row("1.", "Crear entorno virtual de Python")
intro.add_row("2.", "Instalar las librerías del agente")
intro.add_row("3.", "Configurar tus API keys de forma segura")
intro.add_row("4.", "Verificar que todo funcione")

console.print(Panel(
    intro,
    title="[bold]Esto es lo que vamos a hacer[/bold]",
    border_style="dim",
    box=box.ROUNDED,
    padding=(1, 3),
))


# ── Paso 1 — Entorno virtual ──────────────────────────────────────────────────

step(1, "Entorno virtual")

info(
    "Un [bold]entorno virtual[/bold] es una carpeta aislada donde viven las librerías\n"
    "    de este proyecto. Sin él, instalar librerías en tu Python global mezcla\n"
    "    versiones entre proyectos y genera errores difíciles de rastrear.\n"
    "    Con el entorno virtual, este proyecto tiene exactamente lo que necesita."
)
console.print()

if not os.path.isdir(VENV_DIR):
    run_silent([PYTHON, "-m", "venv", VENV_DIR], "Creando entorno virtual...")
    ok("Entorno virtual creado en [cyan]./venv[/cyan]")
else:
    ok("[dim]El entorno virtual ya existe — lo reutilizamos.[/dim]")


# ── Paso 2 — Dependencias ─────────────────────────────────────────────────────

step(2, "Instalación de librerías")

deps = Table(box=box.SIMPLE, padding=(0, 2), show_header=False)
deps.add_column(style="cyan bold", no_wrap=True)
deps.add_column(style="dim")
deps.add_row("python-telegram-bot", "habla con la API de Telegram por nosotros")
deps.add_row("google-genai",        "cliente oficial de Gemini 2.0 (Google AI)")
deps.add_row("groq",                "cliente de Groq — corre Llama 3.1 con hardware especializado")
deps.add_row("python-dotenv",       "carga el archivo .env como variables de entorno")
deps.add_row("rich",                "la librería que hace que esta terminal se vea así")

console.print(Padding(deps, (0, 0, 1, 4)))

info(
    "[dim]Nota:[/dim] si tenés [dim]google-generativeai[/dim] instalado, lo desinstalamos primero.\n"
    "    El modelo [cyan]gemini-2.0-flash[/cyan] requiere la SDK nueva ([cyan]google-genai[/cyan])."
)
console.print()

run_silent(
    [VENV_PIP, "uninstall", "google-generativeai", "-y"],
    "Limpiando SDK vieja de Google (si existía)...",
)
run_silent(
    [VENV_PIP, "install", "-r", "requirements.txt", "-q"],
    "Instalando dependencias...",
)

ok("Librerías instaladas correctamente.")


# ── Paso 3 — API Keys ─────────────────────────────────────────────────────────

step(3, "Tus API keys")

console.print(Panel(
    Text.from_markup(
        "[bold]¿Qué es una API key?[/bold]\n\n"
        "Es una credencial que te identifica ante un servicio externo. Cada vez\n"
        "que el bot le habla a Gemini o Groq, manda esa key en el request. El\n"
        "servicio la valida y sabe que sos vos — no otra persona usando su plataforma.\n\n"
        "[bold]¿Dónde se guardan?[/bold]\n\n"
        "En un archivo [cyan].env[/cyan] en esta carpeta. Una key por línea. Al arrancar\n"
        "el bot, [cyan]python-dotenv[/cyan] lo lee y convierte cada línea en una variable\n"
        "de entorno. El código accede con [cyan]os.getenv('NOMBRE')[/cyan] — nunca\n"
        "escribe el valor directamente.\n\n"
        "[bold]¿Por qué no en el código?[/bold]\n\n"
        "Porque el código va a GitHub. Si la key estuviera ahí, cualquiera podría\n"
        "clonar el repo y hacer requests a tu nombre — con tu cuota y, si tuvieras\n"
        "un plan pago, con tu plata. El [cyan].env[/cyan] está en [cyan].gitignore[/cyan]:\n"
        "nunca se sube. GitHub solo ve el nombre de la variable, no el valor.\n\n"
        "[bold red]Regla de oro:[/bold red] [red]una key en un repo público hay que\n"
        "considerarla comprometida. Revocá y regenerá siempre.[/red]"
    ),
    title="[bold yellow]  Sobre las API keys — leé esto primero  [/bold yellow]",
    border_style="yellow",
    box=box.ROUNDED,
    padding=(1, 3),
))

# Leer keys existentes
existing = {}
if os.path.isfile(".env"):
    for line in open(".env").readlines():
        line = line.strip()
        if "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1)
            existing[k.strip()] = v.strip()

def ask_key(name: str, what: str, where: str, why: str) -> str:
    console.print()
    console.print(Panel(
        Text.from_markup(
            f"[bold]{name}[/bold]\n\n"
            f"{what}\n\n"
            f"[dim]¿Para qué sirve?[/dim]\n{why}\n\n"
            f"[dim]Dónde obtenerla →[/dim] [cyan]{where}[/cyan]"
        ),
        border_style="yellow",
        box=box.ROUNDED,
        padding=(1, 3),
    ))
    while True:
        value = console.input(Padding(
            f"[bold yellow]Pegá el valor aquí:[/bold yellow] ",
            (0, 0, 0, 4),
        )).strip()
        if value:
            return value
        console.print(Padding("[red]No pegaste nada. Intentalo de nuevo.[/red]", (0, 0, 0, 4)))

def get_key(name, what, where, why) -> str:
    current = existing.get(name, "")
    if current and not current.startswith("tu_"):
        console.print()
        console.print(Padding(
            f"[dim]✓ [bold]{name}[/bold] ya está configurada.[/dim]",
            (0, 0, 0, 4),
        ))
        value = console.input(Padding(
            f"[dim]  Presioná Enter para conservarla o pegá un valor nuevo: [/dim]",
            (0, 0, 0, 4),
        )).strip()
        return value if value else current
    return ask_key(name, what, where, why)

telegram_token = get_key(
    "TELEGRAM_TOKEN",
    "El token que identifica a tu bot de Telegram.",
    "Telegram → buscá @BotFather → /newbot → seguí los pasos → copiá el token",
    "Sin este token el bot no puede conectarse a Telegram. Es como el usuario y\n"
    "    la contraseña del bot juntos. Cada bot tiene el suyo — no lo compartas.",
)

gemini_key = get_key(
    "GEMINI_API_KEY",
    "La key que te da acceso al modelo Gemini de Google.",
    "aistudio.google.com → Get API key → Create API key",
    "Cada request a Gemini incluye esta key. Google la verifica y descuenta de tu\n"
    "    cuota. El tier gratuito tiene límite por minuto — suficiente para la clase.",
)

groq_key = get_key(
    "GROQ_API_KEY",
    "La key para acceder a Groq, que corre Llama 3.1 con hardware especializado.",
    "console.groq.com → API Keys → Create API key",
    "Groq usa chips LPU (Language Processing Unit) — notablemente más rápidos que\n"
    "    una GPU para inferencia de LLMs. Es el fallback y la opción 'rápido'.",
)

with open(".env", "w") as f:
    f.write(f"TELEGRAM_TOKEN={telegram_token}\n")
    f.write(f"GEMINI_API_KEY={gemini_key}\n")
    f.write(f"GROQ_API_KEY={groq_key}\n")

console.print()
ok("Keys guardadas en [cyan].env[/cyan]")
info("[dim]Este archivo está en .gitignore — nunca se sube a GitHub.[/dim]")


# ── Paso 4 — Verificación ─────────────────────────────────────────────────────

step(4, "Verificación final")

info(
    "Corremos [cyan]verify_setup.py[/cyan] dentro del entorno virtual para confirmar\n"
    "    que cada librería importa y cada key está cargada correctamente."
)
console.print()

result = subprocess.run([VENV_PY, "verify_setup.py"], text=True)

console.print()

if result.returncode == 0:
    activate_cmd = (
        r"venv\Scripts\activate" if IS_WINDOWS else "source venv/bin/activate"
    )
    console.print(Panel(
        Text.from_markup(
            "[bold green]Todo listo.[/bold green]\n\n"
            "Para arrancar el bot:\n\n"
            f"  [bold]{activate_cmd}[/bold]\n"
            "  [bold cyan]python app.py[/bold cyan]"
        ),
        border_style="green",
        box=box.ROUNDED,
        padding=(1, 4),
    ))
else:
    console.print(Panel(
        "[red]Algo falló en la verificación.[/red]\n\n"
        "Revisá los errores de arriba y corregílos antes de arrancar el bot.",
        border_style="red",
        box=box.ROUNDED,
        padding=(1, 4),
    ))

console.print()
