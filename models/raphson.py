from sympy import diff, sympify, Symbol
from sympy.utilities.lambdify import lambdify

def metodo_raphson(funcion_str, x0, tolerancia, max_iter):
    x = Symbol('x')
    try:
        # Interpretamos la función que puede incluir e
        funcion = sympify(funcion_str)
        f = lambdify(x, funcion, modules=["math"])  # Usamos lambdify para generar la función numérica
        
        # Derivada de la función
        derivada = diff(funcion, x)
        f_prime = lambdify(x, derivada, modules=["math"])  # Función para la derivada
    except Exception as e:
        return {"error": f"Error al interpretar la función: {e}"}

    iteraciones = 0
    historial = []
    x_n = x0  # Estimación inicial

    while iteraciones < max_iter:
        # Evaluar la función y su derivada en x_n
        f_xn = f(x_n)
        f_prime_xn = f_prime(x_n)

        # Verificar si la derivada es cero (lo que impediría la división)
        if f_prime_xn == 0:
            return {"error": "La derivada en x_n es cero, no se puede continuar."}

        # Calcular el siguiente valor de x
        x_n_plus_1 = x_n - f_xn / f_prime_xn

        # Calcular la tolerancia
        tolerancia_calculada = abs((x_n_plus_1 - x_n)/x_n_plus_1) * 100

        # Guardar el historial de la iteración
        historial.append({
            "iteracion": iteraciones + 1,
            "raiz": x_n_plus_1,
            "tolerancia": tolerancia_calculada
        })

        # Comprobar si se alcanzó la tolerancia deseada
        if tolerancia_calculada < tolerancia:
            break

        # Actualizar x_n para la siguiente iteración
        x_n = x_n_plus_1
        iteraciones += 1

    return {
        "raiz": x_n,
        "iteraciones": iteraciones,
        "tolerancia": tolerancia_calculada,
        "historial": historial,
        "exito": True
    }
