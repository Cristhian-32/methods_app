from views.welcome_view import WelcomeView
from views.methods_view import MethodsView
from views.bisection_view import BisectionView
from views.false_postion_view import FalsePositionView
from views.raphson_view import RaphsonView
from views.secante_view import SecanteView
from views.graph_view import GraphView
from models.bisection import metodo_biseccion
from models.false_proposition import metodo_falsa_posicion
from models.raphson import metodo_raphson
from models.secante import metodo_secante
import tkinter as tk
from tkinter import ttk
from sympy import sympify, Symbol
from sympy.utilities.lambdify import lambdify
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np


class AppController:
    def __init__(self, root):
        self.root = root
        self.root.title("Métodos Numéricos")
        self.root.geometry("700x600")
        self.current_view = None
        self.popups_abiertos = []
        self.show_welcome()
    
    def cerrar_popups(self):
        # Recorremos todos los popups abiertos y los cerramos
        for popup in self.popups_abiertos:
            if popup.winfo_exists():
                popup.destroy()
        self.popups_abiertos.clear()

    def show_welcome(self):
        self.clear_view()
        self.current_view = WelcomeView(self.root, self.show_methods)

    def show_methods(self):
        self.clear_view()
        self.current_view = MethodsView(self.root, self.show_bisection, self.show_false_position, self.show_raphson, self.show_secante, self.show_graph)

    def clear_view(self):
        if self.current_view:
            self.current_view.destroy()
    
    def show_bisection(self):
        self.clear_view()
        self.current_view = BisectionView(self.root, self.calculate_bisection, self.buscar_intervalo, self.show_methods)

    def show_false_position(self):
        self.clear_view()
        self.current_view = FalsePositionView(self.root, self.calculate_false_position, self.buscar_intervalo, self.show_methods)

    def show_raphson(self):
        self.clear_view()
        self.current_view = RaphsonView(self.root, self.calculate_raphson, self.show_methods)

    def show_secante(self):
        self.clear_view()
        self.current_view = SecanteView(self.root, self.calculate_secante, self.show_methods)

    def show_graph(self):
        self.clear_view()
        self.current_view = GraphView(self.root, self.mostrar_grafica_intervalo, self.show_methods)

    def buscar_intervalo(self):
        # Validamos que la vista actual tenga los campos necesarios
        if not hasattr(self.current_view, 'function_entry') or \
        not hasattr(self.current_view, 'a_entry') or \
        not hasattr(self.current_view, 'b_entry'):
            self._show_popup("Error", "La vista actual no permite buscar intervalos.")
            return

        funcion_str = self.current_view.function_entry.get()
        x = Symbol('x')

        try:
            funcion = sympify(funcion_str)
            f = lambdify(x, funcion, modules=["math"])
        except Exception as e:
            self._show_popup("Error", f"No se pudo interpretar la función: {e}")
            return

        candidatos = []
        for i in range(-10, 10):
            xi = i
            xf = i + 1
            try:
                if f(xi) * f(xf) < 0:
                    candidatos.append((xi, xf))
            except Exception:
                continue

        if not candidatos:
            self._show_popup("No encontrado", "No se encontró cambio de signo en el rango [-10, 10].")
            return

        # Elegir el intervalo con menor distancia al 0
        mejor = min(candidatos, key=lambda par: abs(par[0]) + abs(par[1]))
        a, b = mejor

        # Mostrar resultados en los campos correspondientes
        self.current_view.a_entry.delete(0, "end")
        self.current_view.a_entry.insert(0, str(a))
        self.current_view.b_entry.delete(0, "end")
        self.current_view.b_entry.insert(0, str(b))

        self.cerrar_popups()
        self._show_popup("Intervalo encontrado", f"Intervalo más cercano a 0:\na = {a}, b = {b}")

    def _mostrar_grafica(self, f, a, b):
        self.grafica_popup = tk.Toplevel(self.root)  # Guardamos la referencia aquí
        self.grafica_popup.title("Gráfica de la función")
        self.grafica_popup.geometry("600x400")

        fig, ax = plt.subplots(figsize=(6, 4), dpi=100)

        x_vals = np.linspace(a - 2, b + 2, 400)
        try:
            y_vals = [f(x) for x in x_vals]
        except Exception as e:
            self._show_popup("Error", f"No se pudo graficar la función: {e}")
            return

        ax.plot(x_vals, y_vals, label="f(x)")
        ax.axhline(0, color='gray', linestyle='--')  # Línea horizontal en y=0
        ax.axvline(a, color='red', linestyle='--', label=f"a = {int(a) if a.is_integer() else a}")
        ax.axvline(b, color='green', linestyle='--', label=f"b = {int(b) if b.is_integer() else b}")
        ax.set_title("Gráfica de la función en el intervalo")
        ax.legend()

        canvas = FigureCanvasTkAgg(fig, master=self.grafica_popup)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Aquí agregamos la ventana de la gráfica a la lista de popups abiertos
        self.popups_abiertos.append(self.grafica_popup)
    
    def _mostrar_grafica_raphson(self, f, x0):
        self.grafica_popup = tk.Toplevel(self.root)
        self.grafica_popup.title("Gráfica de la función (Newton-Raphson)")
        self.grafica_popup.geometry("600x400")

        fig, ax = plt.subplots(figsize=(6, 4), dpi=100)

        # Definir el rango de la gráfica centrado en x0
        rango = 5  # Puedes ajustar este valor si lo deseas
        x_vals = np.linspace(x0 - rango, x0 + rango, 400)
        
        try:
            y_vals = [f(x) for x in x_vals]
        except Exception as e:
            self._show_popup("Error", f"No se pudo graficar la función: {e}")
            return

        ax.plot(x_vals, y_vals, label="f(x)")
        ax.axhline(0, color='gray', linestyle='--')  # Línea horizontal en y=0
        ax.axvline(x0, color='blue', linestyle='--', label=f"x₀ = {int(x0) if x0.is_integer() else x0}")
        ax.set_title("Gráfica de la función alrededor de x₀")
        ax.legend()

        canvas = FigureCanvasTkAgg(fig, master=self.grafica_popup)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.popups_abiertos.append(self.grafica_popup)

    def _mostrar_grafica_intervalo(self, funcion_str, a, b):
        # Función para graficar dentro de un intervalo específico
        self.grafica_popup = tk.Toplevel(self.root)
        self.grafica_popup.title("Gráfica de la función")
        self.grafica_popup.geometry("600x400")

        # Definir la función matemática usando sympy (como en los otros métodos)
        x = Symbol('x')
        try:
            funcion = sympify(funcion_str)
            f = lambdify(x, funcion, modules=["math"])  # Generamos la función numérica
        except Exception as e:
            self._show_popup("Error", f"No se pudo graficar la función: {e}")
            return

        # Generar los valores de x para el intervalo especificado
        x_vals = np.linspace(a - 2, b + 2, 400)  # Extender un poco el intervalo para mejor visualización
        try:
            y_vals = [f(x_val) for x_val in x_vals]
        except Exception as e:
            self._show_popup("Error", f"No se pudo graficar la función: {e}")
            return

        # Crear la gráfica
        fig, ax = plt.subplots(figsize=(6, 4), dpi=100)
        ax.plot(x_vals, y_vals, label=f"f(x) = {funcion_str}")
        ax.axhline(0, color='gray', linestyle='--')  # Línea horizontal en y=0
        ax.axvline(a, color='red', linestyle='--', label=f"a = {int(a) if a.is_integer() else a}")
        ax.axvline(b, color='green', linestyle='--', label=f"b = {int(b) if b.is_integer() else b}")
        ax.set_title("Gráfica de la función en el intervalo")
        ax.legend()

        # Mostrar la gráfica en el popup
        canvas = FigureCanvasTkAgg(fig, master=self.grafica_popup)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Añadir el popup de la gráfica a la lista de popups abiertos
        self.popups_abiertos.append(self.grafica_popup)
    
    def mostrar_grafica_intervalo(self):
        view = self.current_view  # Obtener la vista actual
        try:
            funcion_str = view.function_entry.get()  # Función ingresada
            a = float(view.a_entry.get())  # Valor de 'a'
            b = float(view.b_entry.get())  # Valor de 'b'
        except ValueError:
            self._show_popup("Error", "Verifica que todos los campos estén correctamente llenos.")
            return

        # Llamar a la función de graficado
        self.cerrar_popups()
        self._mostrar_grafica_intervalo(funcion_str, a, b)


    def calculate_bisection(self):
        view = self.current_view
        try:
            funcion_str = view.function_entry.get()
            a = float(view.a_entry.get())
            b = float(view.b_entry.get())
            tol = float(view.tol_entry.get())
            max_iter = int(view.max_iter_entry.get())
        except ValueError:
            self._show_popup("Error", "Verifica que todos los campos estén correctamente llenos.")
            return

        resultado = metodo_biseccion(funcion_str, a, b, tol, max_iter)

        if "error" in resultado:
            self._show_popup("Error", resultado["error"])
            return

        self.cerrar_popups()

        # Mostrar la gráfica
        funcion = sympify(funcion_str)
        x = Symbol('x')
        f = lambdify(x, funcion, modules=["math"])
        self._mostrar_grafica(f, a, b)
        # Mostrar iteraciones
        self._mostrar_resultados_iteraciones(resultado["historial"])

    def calculate_false_position(self):
        view = self.current_view
        try:
            funcion_str = view.function_entry.get()
            a = float(view.a_entry.get())
            b = float(view.b_entry.get())
            tol = float(view.tol_entry.get())
            max_iter = int(view.max_iter_entry.get())
        except ValueError:
            self._show_popup("Error", "Verifica que todos los campos estén correctamente llenos.")
            return

        # Llamamos al método de la falsa posición desde el modelo
        resultado = metodo_falsa_posicion(funcion_str, a, b, tol, max_iter)

        if "error" in resultado:
            self._show_popup("Error", resultado["error"])
            return

        self.cerrar_popups()

        # Mostrar la gráfica
        funcion = sympify(funcion_str)
        x = Symbol('x')
        f = lambdify(x, funcion, modules=["math"])
        self._mostrar_grafica(f, a, b)
        # Mostrar iteraciones
        self._mostrar_resultados_iteraciones(resultado["historial"])

    def calculate_raphson(self):
        view = self.current_view
        try:
            funcion_str = view.function_entry.get()
            x0 = float(view.x0_entry.get())
            tol = float(view.tol_entry.get())
            max_iter = int(view.max_iter_entry.get())
        except ValueError:
            self._show_popup("Error", "Verifica que todos los campos estén correctamente llenos.")
            return

        # Llamamos al método de la falsa posición desde el modelo
        resultado = metodo_raphson(funcion_str, x0, tol, max_iter)

        if "error" in resultado:
            self._show_popup("Error", resultado["error"])
            return

        self.cerrar_popups()

        # Mostrar la gráfica centrada en x0
        x = Symbol('x')
        f_expr = sympify(funcion_str)
        f = lambdify(x, f_expr, modules=["math"])
        self._mostrar_grafica_raphson(f, x0)
        
        # Mostrar iteraciones
        self._mostrar_resultados_iteraciones(resultado["historial"])

    def calculate_secante(self):
        view = self.current_view
        try:
            funcion_str = view.function_entry.get()
            x0 = float(view.x0_entry.get())
            x1 = float(view.x1_entry.get())
            tol = float(view.tol_entry.get())
            max_iter = int(view.max_iter_entry.get())
        except ValueError:
            self._show_popup("Error", "Verifica que todos los campos estén correctamente llenos.")
            return

        # Llamamos al método de la falsa posición desde el modelo
        resultado = metodo_secante(funcion_str, x0, x1, tol, max_iter)

        if "error" in resultado:
            self._show_popup("Error", resultado["error"])
            return

        self.cerrar_popups()

        # Mostrar la gráfica centrada en x0
        x = Symbol('x')
        f_expr = sympify(funcion_str)
        f = lambdify(x, f_expr, modules=["math"])
        self._mostrar_grafica(f, x0, x1)
        
        # Mostrar iteraciones
        self._mostrar_resultados_iteraciones(resultado["historial"])

    def _mostrar_resultados_iteraciones(self, historial):
        # Crear una nueva ventana para mostrar los resultados
        ventana = tk.Toplevel(self.root)
        ventana.title("Resultados de Iteraciones")
        ventana.geometry("600x400")
        
        # Crear el Treeview para mostrar las iteraciones
        treeview = ttk.Treeview(ventana, columns=("Iteración", "Raíz Aproximada", "Tolerancia (%)"), show="headings")
        treeview.heading("Iteración", text="Iteración")
        treeview.heading("Raíz Aproximada", text="Raíz Aproximada")
        treeview.heading("Tolerancia (%)", text="Tolerancia (%)")
        treeview.pack(fill=tk.BOTH, expand=True)

        # Insertar cada iteración en el Treeview
        for item in historial:
            iteracion = item["iteracion"]
            raiz = item["raiz"]
            tolerancia = item["tolerancia"]

            # Si la tolerancia es "N/A", se mantiene tal cual
            if tolerancia == "N/A":
                tolerancia = "N/A"
            else:
                # Formatear la tolerancia a 6 decimales
                tolerancia = f"{tolerancia:.6f}"  # Asegurarse de mostrar correctamente los decimales

            
             # Formatear la raíz y la tolerancia sin decimales si son enteros
            treeview.insert("", "end", values=(iteracion, f"{int(raiz) if raiz.is_integer() else raiz}", tolerancia))

        # Hacer que la ventana sea redimensionable
        treeview.pack(fill=tk.BOTH, expand=True)
        self.popups_abiertos.append(ventana)

    def _show_popup(self, titulo, mensaje):
        popup = tk.Toplevel(self.root)
        popup.title(titulo)
        popup.geometry("350x150")
        popup.configure(bg="#121212")
        label = tk.Label(popup, text=mensaje, font=("Helvetica", 12), fg="#E0E0E0", bg="#121212")
        label.pack(pady=20, padx=20)

        boton = tk.Button(
            popup,
            text="Cerrar",
            command=popup.destroy,
            font=("Helvetica", 12, "bold"),
            bg="#1F1F1F",
            fg="white",
            activebackground="#333333",
            activeforeground="white",
            bd=0,
            padx=15,
            pady=5
        )
        boton.pack(pady=10)

        self.popups_abiertos.append(popup)


