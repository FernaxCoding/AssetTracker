import tkinter as tk
from home import Home
from controller import Controller
from model import Model

if __name__ == "__main__":
    root = tk.Tk()
    model = Model()
    root.mainloop()
    controller = Controller(model, view := Home(root, model))