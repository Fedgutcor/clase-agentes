# Las notas ahora viven en el perfil de cada usuario (memory/users/{id}.json),
# junto a los hechos de "recuerda que...".
# Este archivo reexporta las funciones de memory.py para que app.py
# no necesite cambiar sus imports.

from memory import add_note as save_note, get_notes as list_notes
