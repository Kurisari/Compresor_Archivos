import tkinter as tk
from tkinter import filedialog, messagebox
import os
import sys
script_dir = os.getcwd()
func_dir = os.path.join(script_dir)
sys.path.append(func_dir)
from func import comprimir
from func import descomprimir

class CompresorArchivoApp:
    def __init__(self, root):
        self.huffman = comprimir.HuffmanTree()
        self.huffmanDecode = descomprimir.HuffmanDecoder()
        self.archivo = ""
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
        self.btn_comprimir = tk.Button(root, text="Comprimir Archivo", command=self.comprimir_archivo, state="disabled")
        self.btn_comprimir.pack(side="left", padx=10)
        self.btn_descomprimir = tk.Button(root, text="Descomprimir Archivo", command=self.descomprimir_archivo, state="disabled")
        self.btn_descomprimir.pack(side="right", padx=10)

    def afirmative_message(self, message):
        messagebox.showinfo("Éxito", message)

    def error_message(self, error):
        messagebox.showerror("Error", f"Se produjo un error: {error}")

    def seleccionar_archivo(self):
        self.archivo = filedialog.askopenfilename(initialdir="/", title="Seleccionar Archivo",
                                            filetypes=(("Todos los archivos", "*.*"), ("Archivos de texto", "*.txt")))
        self.archivo_a_comprimir.set(self.archivo)
        if self.archivo:
            self.btn_comprimir.config(state="normal")
            self.btn_descomprimir.config(state="normal")

    def comprimir_archivo(self):
        try:
            file_name = os.path.splitext(os.path.basename(self.archivo))[0]
            file_path = os.path.dirname(self.archivo)
            output_file = os.path.join(file_path, f"{file_name}_compressed.txt")
            tree_file = os.path.join(file_path, f"{file_name}_huffman_tree.txt")
            self.huffman.process_text(self.archivo)
            self.huffman.generate_huffman_codes(self.huffman.root)
            with open(tree_file, 'wb') as tree_file:
                self.huffman.serialize_huffman_tree(tree_file)
            self.huffman.compress_file(self.archivo, output_file)
            self.afirmative_message("Compresion exitosa")
        except Exception as e:
            self.error_message(e)
    
    def descomprimir_archivo(self):
        try:
            file_name = os.path.splitext(os.path.basename(self.archivo))[0]
            file_path = os.path.dirname(self.archivo)
            output_file = os.path.join(file_path, f"{file_name}_decompressed.txt")
            tree_file = os.path.join(file_path, f"{file_name}_huffman_tree.txt")
            output_file = output_file.replace("_compressed", "")
            tree_file = tree_file.replace("_compressed", "")
            with open(tree_file, 'rb') as tree_file:
                self.huffmanDecode.deserialize_huffman_tree(tree_file)
            self.huffmanDecode.decompress_file(self.archivo, output_file)
            self.afirmative_message("Descompresion exitosa")
        except Exception as e:
            self.error_message(e)

if __name__ == "__main__":
    root = tk.Tk()
    app = CompresorArchivoApp(root)
    root.mainloop()