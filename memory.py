import json
import os

# Cada usuario tiene su propio archivo JSON en esta carpeta.
# El nombre del archivo es el ID de Telegram del usuario.
# Ejemplo: memory/users/123456789.json
USERS_DIR = "memory/users"

def load_user(user_id: str) -> dict:
    """Carga el perfil del usuario. Si no existe, devuelve uno vacío."""
    os.makedirs(USERS_DIR, exist_ok=True)  # crea la carpeta si no existe todavía
    path = f"{USERS_DIR}/{user_id}.json"
    if not os.path.exists(path):
        return {"id": user_id, "notes": [], "facts": []}
    with open(path) as f:
        return json.load(f)

def save_user(user_id: str, data: dict):
    """Guarda el perfil del usuario en disco."""
    os.makedirs(USERS_DIR, exist_ok=True)
    with open(f"{USERS_DIR}/{user_id}.json", "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def add_fact(user_id: str, fact: str):
    """Agrega un hecho al perfil del usuario. No guarda duplicados."""
    user = load_user(user_id)
    if fact not in user["facts"]:
        user["facts"].append(fact)
    save_user(user_id, user)

def get_context(user_id: str) -> str:
    """
    Devuelve los hechos del usuario como texto para incluir en el prompt.
    Si el usuario nunca usó 'recuerda que...', devuelve cadena vacía.
    """
    user = load_user(user_id)
    if not user["facts"]:
        return ""
    facts = "\n".join(f"- {f}" for f in user["facts"])
    # Este texto se inyecta al inicio del prompt para que la IA "recuerde" al usuario
    return f"\nLo que sé del usuario:\n{facts}\n"
