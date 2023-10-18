import tkinter as tk
from tkinter import ttk
from view import View


class Controller:
    def __init__(self, model, root):
        self.model = model
        self.view = View(root, self)

        all_assets = self.model.get_all_assets()
        self.view

    def populate_table(self):
        all_assets = self.model.get_all_assets()
        self.view
