"""
Tool: text_stats
Uso en el bot: "analiza texto: [tu texto aquí]"
Devuelve estadísticas básicas del texto sin llamar a ninguna API.
"""

def analyze_text(text: str) -> str:
    words = text.split()
    sentences = [s.strip() for s in text.replace("!", ".").replace("?", ".").split(".") if s.strip()]
    chars = len(text)
    chars_no_spaces = len(text.replace(" ", ""))
    avg_word_len = sum(len(w) for w in words) / len(words) if words else 0
    read_time = max(1, len(words) // 200)

    return (
        f"📊 Estadísticas del texto:\n"
        f"• Palabras: {len(words)}\n"
        f"• Oraciones: {len(sentences)}\n"
        f"• Caracteres: {chars} ({chars_no_spaces} sin espacios)\n"
        f"• Largo promedio de palabra: {avg_word_len:.1f} letras\n"
        f"• Tiempo de lectura estimado: ~{read_time} min"
    )
