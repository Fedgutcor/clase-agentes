import json
import os

USERS_DIR = "memory/users"

def load_user(user_id: str) -> dict:
    os.makedirs(USERS_DIR, exist_ok=True)
    path = f"{USERS_DIR}/{user_id}.json"
    if not os.path.exists(path):
        return {"id": user_id, "notes": [], "facts": []}
    with open(path) as f:
        return json.load(f)

def save_user(user_id: str, data: dict):
    os.makedirs(USERS_DIR, exist_ok=True)
    with open(f"{USERS_DIR}/{user_id}.json", "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def add_fact(user_id: str, fact: str):
    user = load_user(user_id)
    if fact not in user["facts"]:
        user["facts"].append(fact)
    save_user(user_id, user)

def get_context(user_id: str) -> str:
    user = load_user(user_id)
    if not user["facts"]:
        return ""
    facts = "\n".join(f"- {f}" for f in user["facts"])
    return f"\nLo que sé del usuario:\n{facts}\n"
