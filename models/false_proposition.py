from sympy import exp, sympify, Symbol
from sympy.utilities.lambdify import lambdify

def metodo_falsa_posicion(funcion_str, a, b, tolerancia, max_iter):
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
    raiz_anterior = None  # Inicializamos una variable para la raíz anterior
    
    while abs(b - a) > tolerancia and iteraciones < max_iter:
        # Calcular el punto de la falsa posición
        c = (a * f_b - b * f_a) / (f_b - f_a)
        f_c = f(c)

        if f_c == 0:
            break

        # Actualizamos el intervalo
        if f_a * f_c < 0:
            b = c
            f_b = f_c
        else:
            a = c
            f_a = f_c

        iteraciones += 1
        raiz_aproximada = c
        
        # Calcular tolerancia solo si no es la primera iteración
        if raiz_anterior is not None:
            tolerancia_porcentaje = abs(raiz_aproximada - raiz_anterior) * 100
        else:
            tolerancia_porcentaje = None  # No calculamos tolerancia en la primera iteración

        # Guardamos la raíz actual como la anterior para la siguiente iteración
        raiz_anterior = raiz_aproximada
        
        historial.append({
            "iteracion": iteraciones,
            "raiz": raiz_aproximada,
            "tolerancia": tolerancia_porcentaje if tolerancia_porcentaje is not None else "N/A"
        })

    return {
        "raiz": raiz_aproximada,
        "iteraciones": iteraciones,
        "tolerancia": tolerancia_porcentaje,
        "historial": historial,
        "exito": True
    }