import tkinter as tk
from tkinter import ttk
import mysql.connector
import re


class View:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller

        # Geometry, Window title and Page title
        root.geometry("1280x640")
        root.title("Asset Tracker")
        title_label = tk.Label(root, text="Asset Tracker", font=("Helvetica", 24))
        title_label.pack(pady=20)

        def open_add():

            def submit(sys_name, model, manufacturer, type, ip, additional_info, purchase):

                def destroy_add():
                    add.destroy()
                    success_window.destroy()

                error_label = tk.Label(add, text="Please enter dates in the format yyyy/mm/dd")
                date_format = r"\d{4}/\d{2}/\d{2}"

                if re.match(date_format, purchase):
                    success = controller.insert(sys_name, model, manufacturer, type, ip, additional_info, purchase)

                    success_window = tk.Tk()
                    success_window.geometry("300x300")
                    success_window.title("Asset Added")
                    success_label = tk.Label(success_window, text=success, font=("Helvetica", 24))
                    success_label.pack()

                    quit_button = tk.Button(root, text="OK", command=lambda: destroy_add())
                    quit_button.pack(side="bottom")
                else:
                    error_label.pack()

                controller.insert(
                    sys_name, model, manufacturer, type, ip, additional_info, purchase
                )

            # New window for Add
            add = tk.Tk()
            add.geometry("1280x640")
            add.title("Add Asset")
            title_label = tk.Label(add, text="Add Asset", font=("Helvetica", 24))
            title_label.pack(pady=20)

            sys_name_label = tk.Label(add, text="Enter System Name: ")
            sys_name_label.pack()
            sys_name = tk.Entry(add)
            sys_name.pack()

            model_label = tk.Label(add, text="Enter Model: ")
            model_label.pack()
            model = tk.Entry(add)
            model.pack()

            manufacturer_label = tk.Label(add, text="Enter Manufacturer: ")
            manufacturer_label.pack()
            manufacturer = tk.Entry(add)
            manufacturer.pack()

            type_label = tk.Label(add, text="Enter Type: ")
            type_label.pack()
            type = tk.Entry(add)
            type.pack()

            ip_label = tk.Label(add, text="Enter IP Address: ")
            ip_label.pack()
            ip = tk.Entry(add)
            ip.pack()

            additional_info_label = tk.Label(
                add, text="Enter Additional Info (optional): "
            )
            additional_info_label.pack()
            additional_info = tk.Text(add, width="40", height="10")
            additional_info.pack()

            purchase_label = tk.Label(add, text="Enter Purchase date: ")
            purchase_label.pack()
            purchase = tk.Entry(add)
            purchase.pack()

            sys_name = sys_name.get()
            model = model.get()
            manufacturer = manufacturer.get()
            type = type.get()
            ip = ip.get()
            additional_info = additional_info.get()
            purchase = purchase.get()

        def open_delete():
            print("Filler")

        def open_edit():
            print("Filler")

        # Table with all asset info from database
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
        table.column("#7", width=120)
        table.column("#8", width=0)
        # Populate table with data
        assets = controller.populate_table()

        for row in assets:
            asset_id = row[0]
            asset_info = row[1:]

            table.insert("", "end", text=asset_id, values=asset_info)

        table.pack()

        # Buttons for add, edit, delete

        button_add = tk.Button(root, text="Add asset", command=lambda: open_add())
        button_add.pack()

        button_edit = tk.Button(root, text="Edit asset", command=lambda: open_edit())
        button_edit.pack(side="top")

        button_delete = tk.Button(root, text="Delete asset", command=lambda: open_delete())
        button_delete.pack(side="top")
