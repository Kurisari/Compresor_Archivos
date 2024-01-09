import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import sys
import threading
from queue import Queue
import configparser

# Importaciones locales
script_dir = os.getcwd()
func_dir = os.path.join(script_dir)
sys.path.append(func_dir)
from func import comprimir
from func import descomprimir

class CompresorArchivoApp:
    def __init__(self, root):
        # Inicialización de la interfaz
        self.huffman = comprimir.HuffmanTree()
        self.huffmanDecode = descomprimir.HuffmanDecoder()
        self.last_folder = self.load_last_folder()
        self.archivo = ""
        self.queue = Queue()
        self.root = root
        self.setup_gui()

    def setup_gui(self):
        self.root.title("Compresor de Archivos")
        self.root.iconbitmap(r"src\icon.ico")
        self.root.geometry("300x200")

        # Variables
        self.archivo_a_comprimir = tk.StringVar()

        # Widgets
        self.lbl_archivo = tk.Label(self.root, text="Selecciona el archivo a comprimir:")
        self.lbl_archivo.pack(pady=10)

        self.entry_archivo = tk.Entry(self.root, textvariable=self.archivo_a_comprimir, width=40)
        self.entry_archivo.config(state="disabled")
        self.entry_archivo.pack(pady=10)

        self.btn_seleccionar = tk.Button(self.root, text="Seleccionar Archivo", command=self.seleccionar_archivo)
        self.btn_seleccionar.pack(pady=10)

        self.btn_comprimir = tk.Button(self.root, text="Comprimir Archivo", command=self.comprimir_archivo, state="disabled")
        self.btn_comprimir.pack(side="left", padx=10)

        self.btn_descomprimir = tk.Button(self.root, text="Descomprimir Archivo", command=self.descomprimir_archivo, state="disabled")
        self.btn_descomprimir.pack(side="right", padx=10)

        # Progress bar
        self.progress_window = None
        self.progress_bar = None

    def show_progress_bar(self):
        self.progress_window = tk.Toplevel(self.root)
        self.progress_window.title("Progreso de Compresión")
        self.progress_window.geometry("300x50")
        self.progress_bar = ttk.Progressbar(self.progress_window, orient="horizontal", length=280, mode="determinate")
        self.progress_bar.pack(pady=10)

    def hide_progress_bar(self):
        if self.progress_window:
            self.progress_window.destroy()

    def update_progress_bar(self, value):
        self.progress_bar['value'] = value
        if value >= 100:
            self.hide_progress_bar()

    def afirmative_message(self, message):
        messagebox.showinfo("Éxito", message)

    def error_message(self, error):
        messagebox.showerror("Error", f"Se produjo un error: {error}")

    def load_last_folder(self):
        config = configparser.ConfigParser()
        config.read("config.ini")
        return config.get("Settings", "last_folder", fallback="")

    def save_last_folder(self):
        config = configparser.ConfigParser()
        config["Settings"] = {"last_folder": self.last_folder}
        with open("config.ini", "w") as config_file:
            config.write(config_file)

    def seleccionar_archivo(self):
        initial_dir = self.last_folder if self.last_folder else "/"
        self.archivo = filedialog.askopenfilename(initialdir=initial_dir, title="Seleccionar Archivo",
                                                filetypes=(("Todos los archivos", "*.*"),
                                                            ("Archivos de texto", "*.txt;*.crtxt"),
                                                            ("Archivos de imagen", "*.png;*.jpg;*.jpeg;*.crpng;*.crjpg;*.crjpeg"),
                                                            ("Archivos de video", "*.mp4;*.avi;*.mkv;*.crmp4;*.cravi;*.crmkv"),
                                                            ("Archivos de audio", "*.mp3;*.wav;*.ogg;*.crmp3;*.crwav;*.crogg")))
        self.archivo_a_comprimir.set(self.archivo)
        if self.archivo:
            self.last_folder = os.path.dirname(self.archivo)
            self.save_last_folder()
            self.archivo_a_comprimir.set(self.archivo)
            self.btn_comprimir.config(state="normal")
            self.btn_descomprimir.config(state="normal")

    def comprimir_archivo(self):
        try:
            self.show_progress_bar()
            threading.Thread(target=self.ejecutar_compresion).start()
            self.root.after(100, self.check_queue)
        except Exception as e:
            self.hide_progress_bar()
            self.error_message(e)

    def ejecutar_compresion(self):
        try:
            file_name, file_extension = os.path.splitext(os.path.basename(self.archivo))
            file_path = os.path.dirname(self.archivo)
            output_file, tree_file = self.get_output_and_tree_paths(file_name, file_extension, file_path)

            if file_extension.lower() == ".txt":
                self.process_text_file(file_name, file_extension, file_path, output_file, tree_file)
            elif file_extension.lower() in [".png", ".jpg", ".jpeg"]:
                self.process_image_file(file_name, file_extension, file_path, output_file, tree_file)
            elif file_extension.lower() in [".mp4", ".avi", ".mkv"]:
                self.process_video_file(file_name, file_extension, file_path, output_file, tree_file)
            elif file_extension.lower() in [".mp3", ".wav", ".ogg"]:
                self.process_audio_file(file_name, file_extension, file_path, output_file, tree_file)
            else:
                raise ValueError("Unsupported file type")

            self.afirmative_message("Compresion exitosa")
            self.hide_progress_bar()
        except Exception as e:
            self.error_message(e)

    def process_text_file(self, file_name, file_extension, file_path, output_file, tree_file):
        self.huffman.process_text(self.archivo)
        self.huffman.generate_huffman_codes(self.huffman.root)
        self.progress()
        with open(tree_file, 'wb') as tree_file:
            self.huffman.serialize_huffman_tree(tree_file)
        self.huffman.compress_file(self.archivo, output_file)

    def process_image_file(self, file_name, file_extension, file_path, output_file, tree_file):
        char_freq = self.huffman.process_image(self.archivo)
        self.huffman_img = comprimir.HuffmanTree(char_freq)
        self.huffman_img.generate_huffman_codes(self.huffman_img.root)
        self.progress()
        with open(tree_file, 'wb') as tree_file:
            self.huffman_img.serialize_huffman_tree(tree_file)
        self.huffman_img.compress_img_file(self.archivo, output_file)

    def process_video_file(self, file_name, file_extension, file_path, output_file, tree_file):
        frames = self.huffman.process_video(self.archivo)
        self.huffman_vid = comprimir.HuffmanTree(frames)
        self.huffman_vid.generate_huffman_codes(self.huffman_vid.root)
        self.progress()
        with open(tree_file, 'wb') as tree_file:
            self.huffman_vid.serialize_huffman_tree(tree_file)
        self.huffman_vid.compress_video_file(self.archivo, output_file)

    def process_audio_file(self, file_name, file_extension, file_path, output_file, tree_file):
        char_freq = self.huffman.process_audio(self.archivo)
        self.huffman_audio = comprimir.HuffmanTree(char_freq)
        self.huffman_audio.generate_huffman_codes(self.huffman_audio.root)
        self.progress()
        with open(tree_file, 'wb') as tree_file:
            self.huffman_audio.serialize_huffman_tree(tree_file)
        self.huffman_audio.compress_audio_file(self.archivo, output_file)

    def descomprimir_archivo(self):
        try:
            self.show_progress_bar()
            threading.Thread(target=self.ejecutar_descompresion).start()
            self.root.after(100, self.check_queue)
        except Exception as e:
            self.hide_progress_bar()
            self.error_message(e)

    def ejecutar_descompresion(self):
        try:
            file_name, file_extension = os.path.splitext(os.path.basename(self.archivo))
            file_path = os.path.dirname(self.archivo)
            output_file, tree_file = self.get_output_and_tree_paths_decompress(file_name, file_extension, file_path)

            if file_extension.lower() == ".crtxt":
                self.process_text_decompression(tree_file, output_file)
            elif file_extension.lower() in [".crpng", ".crjpg", ".crjpeg"]:
                self.process_image_decompression(tree_file, output_file)
            elif file_extension.lower() in [".crmp4", ".cravi", ".crmkv"]:
                self.process_video_decompression(tree_file, output_file)
            elif file_extension.lower() in [".crmp3", ".crwav", ".crogg"]:
                self.process_audio_decompression(tree_file, output_file)
            else:
                raise ValueError("Unsupported file type")

            self.afirmative_message("Descompresion exitosa")
            self.hide_progress_bar()
        except Exception as e:
            self.hide_progress_bar()
            self.error_message(e)

    def process_text_decompression(self, tree_file, output_file):
        self.progress()
        with open(tree_file, 'rb') as tree_file:
            self.huffmanDecode.deserialize_huffman_tree(tree_file)
        self.huffmanDecode.decompress_file(self.archivo, output_file)

    def process_image_decompression(self, tree_file, output_file):
        self.progress()
        with open(tree_file, 'rb') as tree_file:
            self.huffmanDecode.deserialize_huffman_tree(tree_file)
        self.huffmanDecode.decompress_img_file(self.archivo, output_file)

    def process_video_decompression(self, tree_file, output_file):
        self.progress()
        with open(tree_file, 'rb') as tree_file:
            self.huffmanDecode.deserialize_huffman_tree(tree_file)
        self.huffmanDecode.decompress_vid_file(self.archivo, output_file)

    def process_audio_decompression(self, tree_file, output_file):
        self.progress()
        with open(tree_file, 'rb') as tree_file:
            self.huffmanDecode.deserialize_huffman_tree_aud(tree_file)
        self.huffmanDecode.decompress_audio_file(self.archivo, output_file)

    def get_output_and_tree_paths(self, file_name, file_extension, file_path):
        compressed_suffix = "_compressed"
        custom_extension = file_extension.replace(".", ".cr")
        output_file = os.path.join(file_path, f"{file_name}{compressed_suffix}{custom_extension}")
        tree_file = os.path.join(file_path, f"{file_name}_huffman_tree.txt")
        return output_file, tree_file

    def get_output_and_tree_paths_decompress(self, file_name, file_extension, file_path):
        decompressed_suffix = "_decompressed"
        extension = file_extension.replace(".cr", ".")
        output_file = os.path.join(file_path, f"{file_name}{decompressed_suffix}{extension}")
        tree_file = os.path.join(file_path, f"{file_name}_huffman_tree.txt")
        tree_file = tree_file.replace("_compressed", "")
        return output_file, tree_file

    def progress(self):
        for progress_value in range(100):
            self.queue.put(progress_value)
            self.progress_bar.update_idletasks()
            self.progress_bar.after(1)

    def check_queue(self):
        while not self.queue.empty():
            progress_value = self.queue.get()
            self.update_progress_bar(progress_value)
        self.root.after(100, self.check_queue)

if __name__ == "__main__":
    root = tk.Tk()
    app = CompresorArchivoApp(root)
    root.mainloop()