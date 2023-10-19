import tkinter as tk
from tkinter import ttk
import mysql.connector


class View:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller

        root.geometry("1280x640")
        root.title("Asset Tracker")
        title_label = tk.Label(root, text="Asset Tracker", font=("Helvetica", 24))
        title_label.pack(pady=20)

        # Search bar

        def open_add():
            print("Filler")

        def open_delete():
            print("Filler")

        def open_edit():
            print("Filler")

        table = ttk.Treeview(
            root,
            columns=(
                "System ID",
                "System Name",
                "Model",
                "Manufacturer",
                "Type",
                "IP Address",
                "Additional Information",
                "Purchase Date",
            ),
        )

        table.heading("#0", text="System ID")
        table.heading("#1", text="System Name")
        table.heading("#2", text="Model")
        table.heading("#3", text="Manufacturer")
        table.heading("#4", text="Type")
        table.heading("#5", text="IP Address")
        table.heading("#6", text="Additional Information")
        table.heading("#7", text="Purchase Date")

        table.column("#0", width=100)
        table.column("#1", width=100)
        table.column("#2", width=100)
        table.column("#3", width=100)
        table.column("#4", width=100)
        table.column("#5", width=100)
        table.column("#6", width=200)
        table.column("#7", width=100)

        # Populate table with data
        assets = controller.populate_table()

        for row in assets:
            asset_id = row[0]
            asset_info = row[1:]

            table.insert("", "end", text=asset_id, values=asset_info)

        table.pack()
