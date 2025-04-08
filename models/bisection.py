from sympy import exp, sympify, Symbol
from sympy.utilities.lambdify import lambdify

def metodo_biseccion(funcion_str, a, b, tolerancia, max_iter):
    x = Symbol('x')
    try:
        # Interpretamos la función que puede incluir e
        funcion = sympify(funcion_str)
        f = lambdify(x, funcion, modules=["math"])  # Usamos lambdify para generar la función numérica
    except Exception as e:
        return {"error": f"Error al interpretar la función: {e}"}

    # Asegúrate de evaluar f(a) y f(b) como valores numéricos
    f_a = f(a)
    f_b = f(b)
    
    # Verifica el cambio de signo
    if f_a * f_b >= 0:
        return {"error": "f(a) y f(b) deben tener signos opuestos."}

    iteraciones = 0
    historial = []
    while (b - a) / 2 > tolerancia and iteraciones < max_iter:
        c = (a + b) / 2
        f_c = f(c)
        if f_c == 0:
            break
        elif f_a * f_c < 0:
            b = c
            f_b = f_c
        else:
            a = c
            f_a = f_c
        iteraciones += 1

        raiz_aproximada = (a + b) / 2
        tolerancia_porcentaje =  ((b - a) / 2)*100# Lo convertimos a porcentaje

        historial.append({
            "iteracion": iteraciones,
            "raiz": raiz_aproximada,
            "tolerancia": tolerancia_porcentaje
        })

    return {
        "raiz": raiz_aproximada,
        "iteraciones": iteraciones,
        "tolerancia": tolerancia_porcentaje,
        "historial": historial,
        "exito": True
    }

