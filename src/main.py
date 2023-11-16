import tkinter as tk

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Compresor de Archivos")
        self.geometry("700x600")

app = Application()
app.mainloop()