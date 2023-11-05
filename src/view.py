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

            def submit(sys_name, model, manufacturer, type, ip, additional_info, purchase, employee):
                
                sys_name = sys_name.get()
                model = model.get()
                manufacturer = manufacturer.get()
                type = type.get()
                ip = ip.get()
                additional_info = additional_info.get("1.0", "end")
                purchase = purchase.get()
                employee = employee.get()

                date_format = r"(\d{4})-(\d{2})-(\d{2})" 
                ip_format = r'^(\d{1,3}\.){3}\d{1,3}$'

                if re.match(date_format, purchase) and re.match(ip_format, ip) and sys_name and model and manufacturer and type and ip and employee:
                    success = controller.insert(sys_name, model, manufacturer, type, ip, additional_info, purchase, employee)
                    add.destroy()
                    success_window = tk.Tk()
                    success_window.geometry("300x300")
                    success_window.title("Asset Added")
                    success_label = tk.Label(success_window, text=success, font=("Helvetica", 8))
                    success_label.pack()

                    quit_button = tk.Button(success_window, text="OK", command=lambda: success_window.destroy())
                    quit_button.pack(side="bottom")
                elif(not re.match(date_format, purchase)):
                    error_label_date.config(text="Please enter dates in the format yyyy-mm-dd")
                elif(not re.match(ip_format, ip)):
                    error_label_ip.config(text="Please enter IP in the format XXX.XXX.XXX.XXX")
                else:
                    error_label_fill.config(text="Make sure all the relevent fields are populated")

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

            employee_label = tk.Label(add, text="Choose Employee (by ID): ")
            employee_label.pack()
            employees = controller.get_all_employees()
            selected_employee = tk.StringVar()
            employee = ttk.Combobox(add, textvariable=selected_employee, values=employees, state="readonly")
            employee.pack()

            error_label_date = tk.Label(add, text="")
            error_label_ip = tk.Label(add, text="")
            error_label_fill = tk.Label(add, text="")
            error_label_date.pack()
            error_label_ip.pack()
            error_label_fill()

            submit_button = tk.Button(add, text="Submit", command=lambda: submit(sys_name, model, manufacturer, type, ip, additional_info, purchase, employee))
            submit_button.pack(side="bottom")

        def open_delete():
            def delete_window(asset):
                def kill():
                    confirm_delete.destroy()
                    delete.destroy()

                def delete_asset(asset):
                    # Send data to be deleted to model
                    response = self.controller.delete_asset(asset)
                    response_label = tk.Label(confirm_delete, text=response, font=("Helvetica", 8))
                    response_label.pack()
                    quit = tk.Button(delete, text="Quit", command=lambda: kill())
                    quit.pack()
                
                
                # Confirmation window 
                asset = asset.get()
                if (asset):
                    retreived_asset = self.controller.get_asset_by_id(asset)

                    confirm_delete = tk.Tk()
                    confirm_delete.geometry("1280x640")
                    confirm_delete.title("Choose Asset")
                    title_label = tk.Label(confirm_delete, text="Are you sure you want to delete this asset?", font=("Helvetica", 24))
                    title_label.pack(pady=20)

                    # Deletes Asset
                    yes = tk.Button(confirm_delete, text="Yes", command=lambda: delete_asset(retreived_asset))
                    yes.pack()
                    # Returns to menu
                    no = tk.Button(confirm_delete, text="No", command=lambda: kill())
                    no.pack()
                else:
                    err.config(text="Please make sure you choose an asset")
            # Confirmation window 
            delete = tk.Tk()
            delete.geometry("1280x640")
            delete.title("Delete Asset")
            title_label = tk.Label(delete, text="Delete Asset", font=("Helvetica", 24))
            title_label.pack(pady=20)

            asset_label = tk.Label(delete, text="Choose Asset")
            asset_label.pack()
            assets = controller.get_all_assets()
            selected_asset = tk.StringVar()
            asset = ttk.Combobox(delete, textvariable=selected_asset, values=assets, state="readonly")
            asset.pack()

            err = tk.Label(delete, text="")
            err.pack()

            submit_button = tk.Button(delete, text="Submit", command=lambda: delete_window(asset))
            submit_button.pack(side="bottom")

        def open_edit():
            def edit_window(asset):
                def submit_changes(id, sys_name, model, manufacturer, type, ip, additional_info, purchase, employee):
                    
                    sys_name = sys_name.get()
                    model = model.get()
                    manufacturer = manufacturer.get()
                    type = type.get()
                    ip = ip.get()
                    additional_info = additional_info.get("1.0", "end")
                    purchase = purchase.get()
                    employee = employee.get()
                    employee_id = employee[0]

                    date_format = r"(\d{4})-(\d{2})-(\d{2})" 
                    ip_format = r'^(\d{1,3}\.){3}\d{1,3}$'

                    if re.match(date_format, purchase) and re.match(ip_format, ip) and sys_name and model and manufacturer and type and ip and employee:
                        success = controller.update(id, sys_name, model, manufacturer, type, ip, additional_info, purchase, employee_id)

                        success_label = tk.Label(submit, text=success, font=("Helvetica", 8))
                        success_label.pack()

                        quit_button = tk.Button(submit, text="OK", command=lambda: submit.destroy())
                        quit_button.pack(side="bottom")
                    elif(not re.match(date_format, purchase)):
                        error_label_date.config(text="Please enter dates in the format yyyy-mm-dd")
                    elif(not re.match(ip_format, ip)):
                        error_label_ip.config(text="Please enter IP in the format XXX.XXX.XXX.XXX")
                    else:
                        error_label_fill.config(text="Make sure all the relevent fields are populated")

                asset = asset.get()
                if (asset):
                    retreived_asset = self.controller.get_asset_by_id(asset)

                    submit = tk.Tk()
                    submit.geometry("1280x640")
                    submit.title("Edit Asset")
                    title_label = tk.Label(submit, text="Edit Asset", font=("Helvetica", 24))
                    title_label.pack(pady=20)
                    
                    sys_name_label = tk.Label(submit, text="Enter System Name: ")
                    sys_name_label.pack()
                    sys_name = tk.Entry(submit)
                    sys_name.pack()
                    sys_name.insert(0, retreived_asset[1])

                    model_label = tk.Label(submit, text="Enter Model: ")
                    model_label.pack()
                    model = tk.Entry(submit)
                    model.pack()
                    model.insert(0, retreived_asset[2])

                    manufacturer_label = tk.Label(submit, text="Enter Manufacturer: ")
                    manufacturer_label.pack()
                    manufacturer = tk.Entry(submit)
                    manufacturer.pack()
                    manufacturer.insert(0, retreived_asset[3])

                    type_label = tk.Label(submit, text="Enter Type: ")
                    type_label.pack()
                    type = tk.Entry(submit)
                    type.pack()
                    type.insert(0, retreived_asset[4])

                    ip_label = tk.Label(submit, text="Enter IP Address: ")
                    ip_label.pack()
                    ip = tk.Entry(submit)
                    ip.pack()
                    ip.insert(0, retreived_asset[5])

                    additional_info_label = tk.Label(submit, text="Enter Additional Info (optional): ")
                    additional_info_label.pack()
                    additional_info = tk.Text(submit, width="40", height="10")
                    additional_info.pack()
                    additional_info.insert("1.0", (retreived_asset[6],))

                    purchase_label = tk.Label(submit, text="Enter Purchase date: ")
                    purchase_label.pack()
                    purchase = tk.Entry(submit)
                    purchase.pack()
                    purchase.insert(0, retreived_asset[7])

                    employee_label = tk.Label(submit, text="Choose Employee (by ID): ")
                    employee_label.pack()
                    employees = controller.get_all_employees()
                    selected_employee = tk.StringVar()
                    employee = ttk.Combobox(submit, textvariable=selected_employee, values=employees, state="readonly")
                    employee.pack()
                    employee.set((retreived_asset[8],))

                    id = retreived_asset[0]

                    error_label_date = tk.Label(submit, text="")
                    error_label_ip = tk.Label(submit, text="")
                    error_label_fill = tk.Label(submit, text="")
                    error_label_date.pack()
                    error_label_ip.pack()
                    error_label_fill.pack()

                    submit_button_2 = tk.Button(submit, text="Submit", command=lambda: submit_changes(id, sys_name, model, manufacturer, type, ip, additional_info, purchase, employee))
                    submit_button_2.pack(side="bottom")
                else:
                    err.config(text="Please choose an asset")
                    
            edit = tk.Tk()
            edit.geometry("1280x640")
            edit.title("Choose Asset")
            title_label = tk.Label(edit, text="Choose Asset", font=("Helvetica", 24))
            title_label.pack(pady=20)

            asset_label = tk.Label(edit, text="Choose Asset")
            asset_label.pack()
            assets = controller.get_all_assets()
            selected_asset = tk.StringVar()
            asset = ttk.Combobox(edit, textvariable=selected_asset, values=assets, state="readonly")
            asset.pack()

            err = tk.Label(edit, text="")
            err.pack()

            submit_button = tk.Button(edit, text="Submit", command=lambda: edit_window(asset))
            submit_button.pack(side="bottom")


        def open_emp():

            def submit(first_name, last_name, email, department):

                def destroy_add():
                    add.destroy()
                    success_window.destroy()

                first_name = first_name.get()
                last_name = last_name.get()
                email = email.get()
                department = department.get()

                if (not first_name == "" and not last_name == "" and not email == "" and not department == ""):
                    success = controller.add_employee(first_name, last_name, email, department)

                    success_window = tk.Tk()
                    success_window.geometry("300x300")
                    success_window.title("Employee Added")
                    success_label = tk.Label(success_window, text=success, font=("Helvetica", 8))
                    success_label.pack()

                    quit_button = tk.Button(success_window, text="OK", command=lambda: destroy_add())
                    quit_button.pack(side="bottom")
                else:
                    err.config(text="Make sure all fields are populated")

            # New window for Adding Employee
            add = tk.Tk()
            add.geometry("1280x640")
            add.title("Add Employee")
            title_label = tk.Label(add, text="Add Employee", font=("Helvetica", 24))
            title_label.pack(pady=20)

            first_name_label = tk.Label(add, text="Enter First Name: ")
            first_name_label.pack()
            first_name = tk.Entry(add)
            first_name.pack()

            last_name_label = tk.Label(add, text="Enter Surname: ")
            last_name_label.pack()
            last_name = tk.Entry(add)
            last_name.pack()

            email_label = tk.Label(add, text="Enter Email: ")
            email_label.pack()
            email = tk.Entry(add)
            email.pack()

            department_label = tk.Label(add, text="Select Department: ")
            department_label.pack()

            departments = ['finance', 'human resources', 'operations', 'sales', 'information technology']
            selected_department = tk.StringVar()
            department = ttk.Combobox(add, textvariable=selected_department, values=departments, state="readonly")
            department.pack()

            err = tk.Label(add, text="", font=("Helvetica", 8))
            err.pack()

            submit_button = tk.Button(add, text="Submit", command=lambda: submit(first_name, last_name, email, department))
            submit_button.pack(side="bottom")

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
        table.heading("#8", text="Employee ID")

        table.column("#0", width=100)
        table.column("#1", width=100)
        table.column("#2", width=100)
        table.column("#3", width=100)
        table.column("#4", width=100)
        table.column("#5", width=100)
        table.column("#6", width=200)
        table.column("#7", width=120)
        table.column("#8", width=120)
        # Populate table with data
        assets = controller.get_all_assets()

        for row in assets:
            asset_id = row[0]
            asset_info = row[1:]

            table.insert("", "end", text=asset_id, values=asset_info)

        table.pack()

        # Buttons for add, edit, delete assets

        button_add = tk.Button(root, text="Add asset", command=lambda: open_add())
        button_add.pack()

        button_edit = tk.Button(root, text="Edit asset", command=lambda: open_edit())
        button_edit.pack(side="top")

        button_delete = tk.Button(root, text="Delete asset", command=lambda: open_delete())
        button_delete.pack(side="top")

        # Button for adding employee

        button_emp = tk.Button(root, text="Add Employee", command=lambda: open_emp())
        button_emp.pack(side="top")
