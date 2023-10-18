import tkinter as tk
from view import View
from controller import Controller
from model import Model

if __name__ == "__main__":
    root = tk.Tk()
    model = Model()
    view = View(root)
    controller = Controller(model, view)
    root.mainloop()
