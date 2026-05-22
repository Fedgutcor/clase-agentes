import json
import os

NOTES_FILE = "memory/notes.json"

def _load_all() -> dict:
    if not os.path.exists(NOTES_FILE):
        return {}
    with open(NOTES_FILE) as f:
        return json.load(f)

def save_note(user_id: str, note: str) -> str:
    os.makedirs("memory", exist_ok=True)
    all_notes = _load_all()
    all_notes.setdefault(user_id, []).append(note)
    with open(NOTES_FILE, "w") as f:
        json.dump(all_notes, f, ensure_ascii=False, indent=2)
    return f"Nota guardada: {note}"

def load_notes(user_id: str) -> list:
    return _load_all().get(user_id, [])

def list_notes(user_id: str) -> str:
    notes = load_notes(user_id)
    if not notes:
        return "No tienes notas guardadas."
    return "Tus notas:\n" + "\n".join(f"- {n}" for n in notes)
