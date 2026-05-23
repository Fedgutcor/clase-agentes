import json
import os

# Todas las notas de todos los usuarios se guardan en un solo archivo JSON.
# La estructura es: { "user_id": ["nota 1", "nota 2", ...], ... }
# (La memoria personal de cada usuario está en memory/users/ — son dos sistemas distintos)
NOTES_FILE = "memory/notes.json"

def _load_all() -> dict:
    """Carga todas las notas de todos los usuarios."""
    if not os.path.exists(NOTES_FILE):
        return {}
    with open(NOTES_FILE) as f:
        return json.load(f)

def save_note(user_id: str, note: str) -> str:
    """Agrega una nota a la lista del usuario y la guarda en disco."""
    os.makedirs("memory", exist_ok=True)
    all_notes = _load_all()
    all_notes.setdefault(user_id, []).append(note)  # crea la lista si es la primera nota
    with open(NOTES_FILE, "w") as f:
        json.dump(all_notes, f, ensure_ascii=False, indent=2)
    return f"Nota guardada: {note}"

def load_notes(user_id: str) -> list:
    """Devuelve la lista de notas del usuario (vacía si no tiene ninguna)."""
    return _load_all().get(user_id, [])

def list_notes(user_id: str) -> str:
    """Devuelve las notas del usuario formateadas como texto para enviar por Telegram."""
    notes = load_notes(user_id)
    if not notes:
        return "No tienes notas guardadas."
    return "Tus notas:\n" + "\n".join(f"- {n}" for n in notes)
