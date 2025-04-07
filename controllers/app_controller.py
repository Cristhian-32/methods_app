from views.welcome_view import WelcomeView
from views.methods_view import MethodsView
from views.bisection_view import BisectionView
from views.false_postion_view import FalsePositionView
from models.bisection import metodo_biseccion, buscar_intervalo  # Importamos la nueva función
from models.false_proposition import metodo_falsa_posicion
import tkinter as tk

class AppController:
    def __init__(self, root):
        self.root = root
        self.root.title("Métodos Numéricos")
        self.root.geometry("700x500")
        self.current_view = None
        self.show_welcome()

    def show_welcome(self):
        self.clear_view()
        self.current_view = WelcomeView(self.root, self.show_methods)

    def show_methods(self):
        self.clear_view()
        self.current_view = MethodsView(self.root, self.show_bisection, self.show_false_position)

    def clear_view(self):
        if self.current_view:
            self.current_view.destroy()

    def show_bisection(self):
        self.clear_view()
        self.current_view = BisectionView(self.root, self.calculate_bisection, self.buscar_intervalo, self.show_methods)

    def show_false_position(self):
        self.clear_view()
        self.current_view = FalsePositionView(self.root, self.calculate_false_position, self.buscar_intervalo, self.show_methods)

    def buscar_intervalo(self):
        funcion_str = self.current_view.function_entry.get()
        
        # Llamamos a la nueva función en models/bisection.py
        resultado = buscar_intervalo(funcion_str)

        if "error" in resultado:
            self._show_popup("Error", resultado["error"])
            return

        # Extraemos a y b
        a = resultado["a"]
        b = resultado["b"]

        # Insertar los valores de a y b en los campos
        self.current_view.a_entry.delete(0, "end")
        self.current_view.a_entry.insert(0, str(a))
        self.current_view.b_entry.delete(0, "end")
        self.current_view.b_entry.insert(0, str(b))

        self._show_popup("Intervalo encontrado", f"Intervalo más cercano a 0: a = {a}, b = {b}")

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
        else:
            tolerancia_porcentaje = resultado['tolerancia']
            mensaje = (
                f"Raíz aproximada: {resultado['raiz']}\n"
                f"Iteraciones realizadas: {resultado['iteraciones']}\n"
                f"Tolerancia: {tolerancia_porcentaje:.2f}%"
            )
            self._show_popup("Resultado", mensaje)

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
        else:
            # Si no hay error, mostramos los resultados
            tolerancia_porcentaje = resultado['tolerancia']
            mensaje = (
                f"Raíz aproximada: {resultado['raiz']}\n"
                f"Iteraciones realizadas: {resultado['iteraciones']}\n"
                f"Tolerancia: {tolerancia_porcentaje:.2f}%"
            )
            self._show_popup("Resultado", mensaje)


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
