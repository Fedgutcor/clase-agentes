"""
setup.py — instalación guiada para la clase
Corre con: python setup.py
"""
import os
import sys
import subprocess
import platform

from rich.console import Console
from rich.panel import Panel
from rich.rule import Rule
from rich.text import Text
from rich import box

console = Console()

IS_WINDOWS = platform.system() == "Windows"
PYTHON     = sys.executable
VENV_DIR   = "venv"
VENV_PY    = os.path.join(VENV_DIR, "Scripts" if IS_WINDOWS else "bin", "python")
VENV_PIP   = os.path.join(VENV_DIR, "Scripts" if IS_WINDOWS else "bin", "pip")


# ─────────────────────────────────────────────
#  Helpers
# ─────────────────────────────────────────────

def say(text: str, style: str = ""):
    console.print(f"\n  {text}", style=style)

def step(title: str):
    console.print()
    console.print(Rule(f"[bold cyan]{title}[/bold cyan]", style="cyan"))

def ask_key(name: str, description: str, link: str, why: str) -> str:
    console.print()
    console.print(Panel(
        f"[bold]{name}[/bold]\n\n"
        f"{description}\n\n"
        f"[dim]¿Por qué la necesitamos?[/dim]\n"
        f"{why}\n\n"
        f"[dim]Dónde obtenerla →[/dim] [cyan]{link}[/cyan]",
        border_style="yellow",
        box=box.ROUNDED,
        padding=(1, 3),
    ))
    while True:
        value = console.input("  [bold yellow]Pega el valor aquí:[/bold yellow] ").strip()
        if value:
            return value
        say("[red]No pegaste nada. Inténtalo de nuevo.[/red]")

def write_env(keys: dict):
    with open(".env", "w") as f:
        for k, v in keys.items():
            f.write(f"{k}={v}\n")

def run(cmd: list, label: str):
    say(f"[dim]→ {label}[/dim]")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        console.print(result.stderr)
        console.print(f"\n[red]Error en: {label}[/red]")
        sys.exit(1)


# ─────────────────────────────────────────────
#  Inicio
# ─────────────────────────────────────────────

BANNER = """
 ██████╗ ██╗      █████╗ ███████╗███████╗
██╔════╝ ██║     ██╔══██╗██╔════╝██╔════╝
██║      ██║     ███████║███████╗█████╗
██║      ██║     ██╔══██║╚════██║██╔══╝
╚██████╗ ███████╗██║  ██║███████║███████╗
 ╚═════╝ ╚══════╝╚═╝  ╚═╝╚══════╝╚══════╝

     CONSTRUYE TU PRIMER AGENTE IA
       Setup guiado · python setup.py
"""

console.print(Panel(BANNER, border_style="cyan", box=box.DOUBLE))

say("Hola. Vamos a preparar todo para que el bot funcione en tu máquina.")
say("Este script hace cuatro cosas:")
say("  [cyan]1.[/cyan] Crea un entorno virtual de Python")
say("  [cyan]2.[/cyan] Instala las librerías que el agente necesita")
say("  [cyan]3.[/cyan] Te pide tus API keys y las guarda de forma segura")
say("  [cyan]4.[/cyan] Verifica que todo esté bien antes de arrancar")
say("\nNo tienes que escribir nada raro. Solo seguí las instrucciones.")


# ─────────────────────────────────────────────
#  Paso 1 — Entorno virtual
# ─────────────────────────────────────────────

step("Paso 1 — Entorno virtual")

say("Un [bold]entorno virtual[/bold] es una carpeta aislada donde viven las librerías de este proyecto.")
say("¿Por qué importa? Porque si instalás todo en tu Python global, versiones de distintos")
say("proyectos se pisan entre sí y aparecen errores difíciles de rastrear.")
say("Con el entorno virtual, este proyecto tiene exactamente lo que necesita — nada más.")

if not os.path.isdir(VENV_DIR):
    run([PYTHON, "-m", "venv", VENV_DIR], "Creando entorno virtual...")
    say("[green]✓ Entorno virtual creado en ./venv[/green]")
else:
    say("[dim]✓ El entorno virtual ya existe — lo reutilizamos.[/dim]")


# ─────────────────────────────────────────────
#  Paso 2 — Dependencias
# ─────────────────────────────────────────────

step("Paso 2 — Instalación de librerías")

say("Ahora instalamos las librerías. Cada una tiene un rol específico:\n")
say("  [cyan]python-telegram-bot[/cyan]  →  habla con la API de Telegram por nosotros")
say("  [cyan]google-genai[/cyan]         →  cliente oficial de Gemini (Google AI)")
say("  [cyan]groq[/cyan]                 →  cliente de Groq, que corre Llama 3.1 ultra-rápido")
say("  [cyan]python-dotenv[/cyan]        →  lee el archivo .env y carga las keys como variables")
say("  [cyan]rich[/cyan]                 →  la librería que hace que esta terminal se vea así\n")

say("[dim]Nota técnica:[/dim] desinstalamos [dim]google-generativeai[/dim] si existe — es la SDK vieja.")
say("[dim]El modelo gemini-2.0-flash requiere la nueva ([cyan]google-genai[/cyan]).[/dim]\n")

run([VENV_PIP, "uninstall", "google-generativeai", "-y"],
    "Limpiando SDK vieja de Google (si existía)...")
run([VENV_PIP, "install", "-r", "requirements.txt", "-q"],
    "Instalando dependencias...")

say("[green]✓ Librerías instaladas correctamente.[/green]")


# ─────────────────────────────────────────────
#  Paso 3 — API Keys
# ─────────────────────────────────────────────

step("Paso 3 — Tus API keys")

console.print()
console.print(Panel(
    "[bold]¿Qué es una API key?[/bold]\n\n"
    "Es una contraseña que te identifica ante un servicio externo.\n"
    "Cuando el bot le habla a Gemini o a Groq, manda esa key en cada request.\n"
    "El servicio la valida y sabe que sos vos — y no otra persona usando su plataforma.\n\n"
    "[bold]¿Dónde se guardan?[/bold]\n\n"
    "En un archivo llamado [cyan].env[/cyan] en esta carpeta. Es un archivo de texto plano,\n"
    "una key por línea. Lo lee [cyan]python-dotenv[/cyan] al arrancar el bot y lo convierte\n"
    "en variables de entorno — así el código accede con [cyan]os.getenv('NOMBRE')[/cyan].\n\n"
    "[bold]¿Por qué no está en el código?[/bold]\n\n"
    "Porque el código va a GitHub. Si la key estuviera ahí, cualquiera podría verla,\n"
    "clonar el repo y hacer requests a tu nombre — con tu cuota y, si tuvieras un plan\n"
    "pago, con tu plata. El archivo [cyan].env[/cyan] está en [cyan].gitignore[/cyan]: nunca\n"
    "se sube. El código solo sabe el [italic]nombre[/italic] de la variable, nunca el valor.\n\n"
    "[bold red]Regla de oro:[/bold red] [red]una key que se sube a un repo público debe\n"
    "considerarse comprometida. Revocá y regenerá siempre.[/red]",
    title="[bold yellow]Sobre las API keys — leé esto[/bold yellow]",
    border_style="yellow",
    box=box.ROUNDED,
    padding=(1, 3),
))

# Leer keys existentes si el .env ya existe
existing = {}
if os.path.isfile(".env"):
    for line in open(".env").readlines():
        line = line.strip()
        if "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1)
            existing[k.strip()] = v.strip()

def get_key(name, description, link, why):
    current = existing.get(name, "")
    if current and not current.startswith("tu_"):
        say(f"[dim]✓ {name} ya está configurada. Presioná Enter para conservarla "
            f"o pegá un valor nuevo.[/dim]")
        console.print()
        value = console.input(f"  [bold yellow]{name}:[/bold yellow] [{current[:8]}...] ").strip()
        return value if value else current
    return ask_key(name, description, link, why)

telegram_token = get_key(
    "TELEGRAM_TOKEN",
    "El token que identifica a tu bot de Telegram.",
    "Telegram → busca @BotFather → /newbot → seguí los pasos → copiá el token",
    "Sin este token el bot no puede conectarse a Telegram. Es como el nombre de usuario\n"
    "  y la contraseña del bot juntos. Cada bot tiene el suyo — no lo compartas.",
)

gemini_key = get_key(
    "GEMINI_API_KEY",
    "La key que te da acceso al modelo Gemini de Google.",
    "aistudio.google.com → Get API key → Create API key",
    "Cada vez que el bot le hace una pregunta a Gemini, Google verifica esta key.\n"
    "  El tier gratuito tiene límite de requests por minuto — suficiente para la clase.",
)

groq_key = get_key(
    "GROQ_API_KEY",
    "La key para acceder a Groq, que corre Llama 3.1 con hardware especializado.",
    "console.groq.com → API Keys → Create API key",
    "Groq es el fallback cuando Gemini falla, y la opción 'rápido' del router.\n"
    "  Su infraestructura (LPU) es notablemente más veloz que una GPU convencional.",
)

write_env({
    "TELEGRAM_TOKEN": telegram_token,
    "GEMINI_API_KEY": gemini_key,
    "GROQ_API_KEY":   groq_key,
})

say("[green]✓ Keys guardadas en .env[/green]")
say("[dim]Este archivo no se sube a GitHub — está en .gitignore.[/dim]")


# ─────────────────────────────────────────────
#  Paso 4 — Verificación
# ─────────────────────────────────────────────

step("Paso 4 — Verificación final")

say("Corremos [cyan]verify_setup.py[/cyan] dentro del entorno virtual para confirmar que todo funciona.")
say("[dim]Lo que hace: importa cada librería, lee el .env y valida que las keys estén cargadas.[/dim]\n")

result = subprocess.run([VENV_PY, "verify_setup.py"], capture_output=False, text=True)

console.print()

if result.returncode == 0:
    console.print(Panel(
        "[bold green]Todo listo.[/bold green]\n\n"
        "Para arrancar el bot, activá el entorno virtual y corré [cyan]app.py[/cyan]:\n\n"
        + (
            "  [bold]venv\\Scripts\\activate[/bold]\n"
            "  [bold cyan]python app.py[/bold cyan]"
            if IS_WINDOWS else
            "  [bold]source venv/bin/activate[/bold]\n"
            "  [bold cyan]python app.py[/bold cyan]"
        ),
        border_style="green",
        box=box.ROUNDED,
        padding=(1, 4),
    ))
else:
    console.print(Panel(
        "[red]Algo falló en la verificación.[/red]\n\n"
        "Revisá los errores arriba. Si necesitás ayuda, avisame.",
        border_style="red",
        box=box.ROUNDED,
        padding=(1, 4),
    ))

console.print()
