import tkinter as tk

class WelcomeView(tk.Frame):
    def __init__(self, master, start_callback):
        super().__init__(master, bg="#121212")
        self.pack(expand=True, fill="both")

        self.label = tk.Label(
            self,
            text="Bienvenido a la app de Métodos Numéricos",
            font=("Helvetica", 18),
            fg="#E0E0E0",
            bg="#121212"
        )
        self.label.pack(pady=40)

        self.start_button = tk.Button(
            self,
            text="Empezar",
            command=start_callback,
            font=("Helvetica", 14, "bold"),
            bg="#1F1F1F",
            fg="white",
            activebackground="#333333",
            activeforeground="white",
            bd=0,
            padx=20,
            pady=10
        )
        self.start_button.pack(pady=10)
