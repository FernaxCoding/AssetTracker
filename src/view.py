import tkinter as tk
from tkinter import ttk


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

        table.heading("#1", text="System ID")
        table.heading("#2", text="System Name")
        table.heading("#3", text="Model")
        table.heading("#4", text="Manufacturer")
        table.heading("#5", text="Type")
        table.heading("#6", text="IP Address")
        table.heading("#6", text="Additional Information")
        table.heading("#7", text="Purchase Date")

        table.column("#1", width=100)
        table.column("#2", width=100)
        table.column("#3", width=100)
        table.column("#4", width=100)
        table.column("#5", width=100)
        table.column("#6", width=100)
        table.column("#6", width=200)
        table.column("#7", width=100)

        # Temporary data
        data = [
            (
                "Computer1",
                "Model1",
                "Manufacturer1",
                "Type1",
                "192.168.1.1",
                "Additional Info 1",
                "2023-10-13",
            ),
            (
                "Computer1",
                "Model1",
                "Manufacturer1",
                "Type1",
                "192.168.1.1",
                "Additional Info 1",
                "2023-10-13",
            ),
            (
                "Computer1",
                "Model1",
                "Manufacturer1",
                "Type1",
                "192.168.1.1",
                "Additional Info 1",
                "2023-10-13",
            ),
            (
                "Computer1",
                "Model1",
                "Manufacturer1",
                "Type1",
                "192.168.1.1",
                "Additional Info 1",
                "2023-10-13",
            ),
        ]

        for item in data:
            table.insert("", "end", values=item)

        table.pack()
