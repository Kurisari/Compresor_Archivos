import tkinter as tk
from tkinter import filedialog

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Compresor de Archivos")
        self.geometry("700x600")
        self.boton_buscar = tk.Button(self, text="Buscar Archivo", command=self.buscar_archivo)
        self.boton_buscar.pack()
        self.etiqueta_ruta = tk.Label(self, text="")
        self.etiqueta_ruta.pack()

    def buscar_archivo(self):
        self.ruta_archivo = filedialog.askopenfilename()
        self.etiqueta_ruta.config(text=f"Archivo seleccionado: {self.ruta_archivo}")

app = Application()
app.mainloop()
