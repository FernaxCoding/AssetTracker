import tkinter as tk
from view import View
from controller import Controller
from model import Model

if __name__ == "__main__":
    root = tk.Tk()
    model = Model()
    controller = Controller(model, view := View(root, model))
    root.mainloop()