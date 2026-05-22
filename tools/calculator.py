def calculate(expression: str) -> str:
    try:
        result = eval(expression, {"__builtins__": {}})
        return f"Resultado: {result}"
    except Exception as e:
        return f"No pude calcular eso: {e}"
