import tkinter as tk
from tkinter import ttk
from view import View
from model import Model


class Controller:
    def __init__(self, root):
        self.model = Model()
        self.view = View(root, self)

    # Used to populate the table on the main menu
    def populate_table(self):
        all_assets = self.model.get_all_assets()
        return all_assets

    def insert(
        self, sys_name, model, manufacturer, type, ip, additional_info, purchase
    ):
        return self.model.insert_asset(
            sys_name, model, manufacturer, type, ip, additional_info, purchase
        )
