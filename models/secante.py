from sympy import Symbol, sympify
from sympy.utilities.lambdify import lambdify

def metodo_secante(funcion_str, x0, x1, tolerancia, max_iter):
    x = Symbol('x')
    try:
        funcion = sympify(funcion_str)
        f = lambdify(x, funcion, modules=["math"])
    except Exception as e:
        return {"error": f"Error al interpretar la función: {e}"}

    historial = []
    iteraciones = 0
    error = None

    while iteraciones < max_iter:
        try:
            fx0 = f(x0)
            fx1 = f(x1)
            if fx1 - fx0 == 0:
                return {"error": "División por cero en la fórmula de la secante."}

            x2 = x1 - fx1 * ((x1 - x0) / (fx1 - fx0))
        except Exception as e:
            return {"error": f"Error durante la iteración: {e}"}

        error = abs((x1 - x0) / x1) * 100

        historial.append({
            "iteracion": iteraciones + 1,
            "raiz": x2,
            "tolerancia": error
        })

        if isinstance(error, (float, int)) and error < tolerancia:
            break

        x0, x1 = x1, x2
        iteraciones += 1

    return {
        "raiz": x2,
        "iteraciones": iteraciones,
        "tolerancia": error if isinstance(error, (float, int)) else 0.0,
        "historial": historial,
        "exito": True
    }
