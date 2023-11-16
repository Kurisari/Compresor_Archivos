import tkinter as tk
from tkinter import filedialog
import shutil
import os
from func import comprimir
from func import descomprimir

class CompresorArchivoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Compresor de Archivos")
        root.iconbitmap("H:\My Drive\programacion\Compresor_Archivos\Compresor_Archivos\src\icon.ico")
        self.root.geometry("300x200")
        self.archivo_a_comprimir = tk.StringVar()
        self.lbl_archivo = tk.Label(root, text="Selecciona el archivo a comprimir:")
        self.lbl_archivo.pack(pady=10)
        self.entry_archivo = tk.Entry(root, textvariable=self.archivo_a_comprimir, width=40)
        self.entry_archivo.config(state="disabled")
        self.entry_archivo.pack(pady=10)
        self.btn_seleccionar = tk.Button(root, text="Seleccionar Archivo", command=self.seleccionar_archivo)
        self.btn_seleccionar.pack(pady=10)
        self.btn_comprimir = tk.Button(root, text="Comprimir Archivo", command=self.comprimir_archivo)
        self.btn_comprimir.pack(pady=10)

    def seleccionar_archivo(self):
        archivo = filedialog.askopenfilename(initialdir="/", title="Seleccionar Archivo",
                                            filetypes=(("Todos los archivos", "*.*"), ("Archivos de texto", "*.txt")))
        self.archivo_a_comprimir.set(archivo)

    def comprimir_archivo(self):
        pass

if __name__ == "__main__":
    root = tk.Tk()
    app = CompresorArchivoApp(root)
    root.mainloop()