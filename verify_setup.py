import sys
import os

def check(label, fn):
    try:
        fn()
        print(f"  OK  {label}")
    except Exception as e:
        print(f"  FAIL {label}: {e}")

def assert_python():
    assert sys.version_info >= (3, 10), f"Python {sys.version} — necesitas 3.10+"

def require_env(key):
    val = os.getenv(key)
    if not val or val.startswith("tu_"):
        raise Exception(f"{key} no configurada")

print("\n=== Verificación de setup ===\n")

check("Python >= 3.10", assert_python)
check("python-telegram-bot", lambda: __import__("telegram"))
check("google-generativeai", lambda: __import__("google.generativeai"))
check("groq", lambda: __import__("groq"))
check("python-dotenv", lambda: __import__("dotenv"))
check(".env existe", lambda: open(".env").close())

from dotenv import load_dotenv
load_dotenv()
check("TELEGRAM_TOKEN", lambda: require_env("TELEGRAM_TOKEN"))
check("GEMINI_API_KEY", lambda: require_env("GEMINI_API_KEY"))
check("GROQ_API_KEY", lambda: require_env("GROQ_API_KEY"))

print("\nSi todo dice OK, estás listo para la clase.\n")
