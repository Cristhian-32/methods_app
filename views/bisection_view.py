import tkinter as tk

class BisectionView(tk.Frame):
    def __init__(self, master, calculate_callback, buscar_callback, back_callback):
        super().__init__(master, bg="#121212")
        self.pack(expand=True, fill="both")
        master.title("Método de Bisección")

        # Título
        title = tk.Label(
            self,
            text="Método de Bisección",
            font=("Helvetica", 18, "bold"),
            fg="#E0E0E0",
            bg="#121212"
        )
        title.pack(pady=20)

        # Función
        self.function_entry = self._create_labeled_entry("Función f(x):", "x**3 - x - 2")

        # Intervalo [a, b]
        self.a_entry = self._create_labeled_entry("Valor de a:", "1")
        self.b_entry = self._create_labeled_entry("Valor de b:", "2")

        # Tolerancia
        self.tol_entry = self._create_labeled_entry("Tolerancia:", "0.0001")

        # Iteraciones máximas
        self.max_iter_entry = self._create_labeled_entry("Iteraciones máximas:", "100")

        # Botón para buscar intervalo automáticamente
        buscar_intervalo_button = tk.Button(
            self,
            text="Buscar intervalo automático",
            command=buscar_callback,
            font=("Helvetica", 12),
            bg="#2C2C2C",
            fg="white",
            activebackground="#444444",
            activeforeground="white",
            bd=0,
            padx=15,
            pady=8
        )
        buscar_intervalo_button.pack(pady=10)

        # Botón calcular
        calculate_button = tk.Button(
            self,
            text="Calcular",
            command=calculate_callback,
            font=("Helvetica", 14, "bold"),
            bg="#1F1F1F",
            fg="white",
            activebackground="#333333",
            activeforeground="white",
            bd=0,
            padx=20,
            pady=10
        )
        calculate_button.pack(pady=20)

        # Botón "Atrás" para volver a la vista principal
        back_button = tk.Button(
            self,
            text="Atrás",
            command=back_callback,
            font=("Helvetica", 12),
            bg="#2C2C2C",
            fg="white",
            activebackground="#444444",
            activeforeground="white",
            bd=0,
            padx=15,
            pady=8
        )
        back_button.pack(pady=10)

    def _create_labeled_entry(self, label_text, default_value=""):
        frame = tk.Frame(self, bg="#121212")
        frame.pack(pady=5)

        label = tk.Label(
            frame,
            text=label_text,
            font=("Helvetica", 12),
            fg="#E0E0E0",
            bg="#121212"
        )
        label.pack(side="left", padx=10)

        entry = tk.Entry(
            frame,
            font=("Helvetica", 12),
            bg="#1F1F1F",
            fg="white",
            insertbackground="white",
            width=20
        )
        entry.insert(0, default_value)
        entry.pack(side="left")
        return entry
