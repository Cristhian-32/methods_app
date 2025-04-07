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

    return {
        "raiz": raiz_aproximada,
        "iteraciones": iteraciones,
        "tolerancia": tolerancia_porcentaje,
        "exito": True
    }

def buscar_intervalo(funcion_str):
    x = Symbol('x')

    try:
        funcion = sympify(funcion_str)
        f = lambdify(x, funcion, modules=["math"])
    except Exception as e:
        return {"error": f"No se pudo interpretar la función: {e}"}

    # Exploramos el rango de enteros de -10 a 10
    candidatos = []

    for i in range(-10, 10):
        xi = i
        xf = i + 1
        try:
            if f(xi) * f(xf) < 0:  # Cambio de signo entre i y i+1
                candidatos.append((xi, xf))
        except:
            continue

    if not candidatos:
        return {"error": "No se encontró cambio de signo en el rango [-10, 10]."}

    # Elegir el intervalo más cercano a cero en valor absoluto
    mejor = min(candidatos, key=lambda par: abs(par[0]) + abs(par[1]))
    a, b = mejor

    return {"a": a, "b": b}



