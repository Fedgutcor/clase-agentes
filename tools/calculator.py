def calculate(expression: str) -> str:
    """
    Evalúa una expresión matemática y devuelve el resultado como texto.
    Ejemplos: "45 * 12", "100 / 4 + 3", "2 ** 8"

    eval() ejecuta código Python directamente, por eso es importante el segundo
    argumento: {"__builtins__": {}} desactiva todas las funciones del sistema.
    Sin eso, alguien podría escribir "calcula __import__('os').system('rm -rf /')"
    y borrar archivos. Con esa restricción, solo funcionan operaciones matemáticas.
    """
    try:
        result = eval(expression, {"__builtins__": {}})
        return f"Resultado: {result}"
    except Exception as e:
        return f"No pude calcular eso: {e}"
