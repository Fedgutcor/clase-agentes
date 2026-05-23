import json
import os

# Cada usuario tiene su propio archivo JSON en esta carpeta.
# El nombre del archivo es el ID de Telegram del usuario.
# Ejemplo: memory/users/123456789.json
#
# Estructura del archivo:
# {
#   "id": "123456789",
#   "facts": ["estudia diseño", "vive en Bogotá"],
#   "notes": ["comprar leche", "llamar al médico"],
#   "reminders": [
#     {"message": "llamar al médico", "fires_at": 1716000000.0}
#   ]
# }
# "fires_at" es un timestamp Unix: segundos desde el 1 de enero de 1970.
# Es el formato estándar para guardar momentos en el tiempo — funciona en cualquier zona horaria.
USERS_DIR = "memory/users"

def load_user(user_id: str) -> dict:
    """Carga el perfil del usuario. Si no existe, devuelve uno vacío."""
    os.makedirs(USERS_DIR, exist_ok=True)
    path = f"{USERS_DIR}/{user_id}.json"
    if not os.path.exists(path):
        return {"id": user_id, "facts": [], "notes": [], "reminders": []}
    with open(path) as f:
        return json.load(f)

def save_user(user_id: str, data: dict):
    """Guarda el perfil del usuario en disco."""
    os.makedirs(USERS_DIR, exist_ok=True)
    with open(f"{USERS_DIR}/{user_id}.json", "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ── Hechos (memoria personal) ─────────────────────────────────────────────────

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

# ── Notas ─────────────────────────────────────────────────────────────────────

def add_note(user_id: str, note: str) -> str:
    """Agrega una nota a la lista del usuario y la guarda en disco."""
    user = load_user(user_id)
    user.setdefault("notes", []).append(note)
    save_user(user_id, user)
    return f"Nota guardada: {note}"

def get_notes(user_id: str) -> str:
    """Devuelve las notas del usuario formateadas como texto para Telegram."""
    user  = load_user(user_id)
    notes = user.get("notes", [])
    if not notes:
        return "No tienes notas guardadas."
    return "Tus notas:\n" + "\n".join(f"- {n}" for n in notes)

# ── Recordatorios ─────────────────────────────────────────────────────────────

def save_reminder(user_id: str, message: str, fires_at: float):
    """
    Persiste un recordatorio en el perfil del usuario.
    fires_at: timestamp Unix del momento exacto en que debe dispararse.
    """
    user = load_user(user_id)
    user.setdefault("reminders", []).append({"message": message, "fires_at": fires_at})
    save_user(user_id, user)

def delete_reminder(user_id: str, message: str, fires_at: float):
    """Elimina un recordatorio del perfil una vez que se disparó."""
    user = load_user(user_id)
    user["reminders"] = [
        r for r in user.get("reminders", [])
        if not (r["message"] == message and r["fires_at"] == fires_at)
    ]
    save_user(user_id, user)

def get_all_reminders() -> list[dict]:
    """
    Lee todos los perfiles y devuelve los recordatorios pendientes.
    Se usa al arrancar el bot para reconstruir timers que sobrevivieron un reinicio.
    Devuelve: [{"user_id": "...", "message": "...", "fires_at": 123456.0}, ...]
    """
    pending = []
    if not os.path.exists(USERS_DIR):
        return pending
    for filename in os.listdir(USERS_DIR):
        if not filename.endswith(".json"):
            continue
        user_id = filename[:-5]  # quita el ".json" para obtener el ID
        user    = load_user(user_id)
        for r in user.get("reminders", []):
            pending.append({"user_id": user_id, **r})
    return pending
