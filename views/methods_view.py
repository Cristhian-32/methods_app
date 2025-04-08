import tkinter as tk

class MethodsView(tk.Frame):
    def __init__(self, master, bisection_callback, false_position_callback, raphson_callback, secante_callback):
        super().__init__(master, bg="#121212")
        self.pack(expand=True, fill="both")

        self.label = tk.Label(
            self,
            text="Selecciona un método:",
            font=("Helvetica", 18),
            fg="#E0E0E0",
            bg="#121212"
        )
        self.label.pack(pady=30)

        self.bisection_button = tk.Button(
            self,
            text="Método de Bisección",
            command=bisection_callback,
            font=("Helvetica", 14, "bold"),
            bg="#1F1F1F",
            fg="white",
            activebackground="#333333",
            activeforeground="white",
            bd=0,
            padx=20,
            pady=10
        )
        self.bisection_button.pack(pady=10)

        self.label.pack(pady=30)

        self.false_position_button = tk.Button(
            self,
            text="Método de la Falsa Posición",
            command=false_position_callback,
            font=("Helvetica", 14, "bold"),
            bg="#1F1F1F",
            fg="white",
            activebackground="#333333",
            activeforeground="white",
            bd=0,
            padx=20,
            pady=10
        )
        self.false_position_button.pack(pady=10)

        self.label.pack(pady=30)

        self.raphson_button = tk.Button(
            self,
            text="Método de Newton-Raphson",
            command=raphson_callback,
            font=("Helvetica", 14, "bold"),
            bg="#1F1F1F",
            fg="white",
            activebackground="#333333",
            activeforeground="white",
            bd=0,
            padx=20,
            pady=10
        )
        self.raphson_button.pack(pady=10)

        self.label.pack(pady=30)

        self.secante_button = tk.Button(
            self,
            text="Método de la Secante",
            command=secante_callback,
            font=("Helvetica", 14, "bold"),
            bg="#1F1F1F",
            fg="white",
            activebackground="#333333",
            activeforeground="white",
            bd=0,
            padx=20,
            pady=10
        )
        self.secante_button.pack(pady=10)


    def select_bisection(self):
        print("Bisección seleccionado")
