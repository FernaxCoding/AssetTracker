import tkinter as tk
from tkinter import ttk


class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view

        # All assets from database
        all_assets = model.get_all_assets()
