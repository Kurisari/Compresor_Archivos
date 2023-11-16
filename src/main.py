import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Compresor de Archivos")
        self.geometry("700x600")
        style = ttk.Style()
        style.configure("TButton", padding=10, relief="flat", font=('Helvetica', 12))
        style.configure("TLabel", font=('Helvetica', 12))
        self.boton_buscar = ttk.Button(self, text="Buscar Archivo", command=self.buscar_archivo)
        self.boton_buscar.pack(pady=20)
        self.etiqueta_ruta = ttk.Label(self, text="")
        self.etiqueta_ruta.pack()
        self.boton2 = ttk.Button(self, text="Comprimir", command=self.accion_boton)
        self.boton2.pack(pady=10)
        self.boton3 = ttk.Button(self, text="Descomprimir", command=self.accion_boton)
        self.boton3.pack(pady=10)
        self.boton4 = ttk.Button(self, text="Cancelar", command=self.accion_boton)
        self.boton4.pack(pady=10)

    def buscar_archivo(self):
        self.ruta_archivo = filedialog.askopenfilename()
        self.etiqueta_ruta.config(text=f"Archivo seleccionado: {self.ruta_archivo}")

    def accion_boton(self):
        print("Funcionando")

app = Application()
app.mainloop()
