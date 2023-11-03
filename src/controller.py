import tkinter as tk
from tkinter import ttk
from view import View
from model import Model


class Controller:
    def __init__(self, root):
        self.model = Model()
        self.view = View(root, self)

    # Used to populate the table on the main menu
    def get_all_assets(self):
        all_assets = self.model.get_all_assets()
        return all_assets

    def insert(self, sys_name, model, manufacturer, type, ip, additional_info, purchase, employee):
        return self.model.insert_asset(sys_name, model, manufacturer, type, ip, additional_info, purchase, employee)
    
    def add_employee(self, first_name, last_name, email, department):
        return self.model.add_employee(first_name, last_name, email, department)
    
    def get_all_employees(self):
        return self.model.get_all_employees()
    
    def get_asset_by_id(self, id):
        return self.model.get_asset_by_id(id)
    
    def update(self, id, sys_name, model, manufacturer, type, ip, additional_info, purchase, employee_id):
        return self.model.edit_asset(id, sys_name, model, manufacturer, type, ip, additional_info, purchase, employee_id)


