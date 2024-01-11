from view import View
from model import Model

class Controller:
    def __init__(self, root):
        self.model = Model()
        self.view = View(root, self)

    # Used to populate the table on the main menu
    def get_all_assets(self, table):
        all_assets = self.model.get_all_assets(table)
        return all_assets

    def insert(self, sys_name, model, manufacturer, type, ip, additional_info, purchase, employee):
        return self.model.insert_asset(sys_name, model, manufacturer, type, ip, additional_info, purchase, employee)
    
    def insert_software(self, sys_name, version, manufacturer):
        return self.model.insert_asset_software(sys_name, version, manufacturer)
    
    def add_employee(self, first_name, last_name, email, department, password, re_password):
        return self.model.add_employee(first_name, last_name, email, department, password, re_password)
    
    def get_all_employees(self):
        return self.model.get_all_employees()
    
    def get_asset_by_id(self, id, table):
        return self.model.get_asset_by_id(id, table)
    
    def update(self, id, sys_name, model, manufacturer, type, ip, additional_info, purchase, employee_id):
        return self.model.edit_asset(id, sys_name, model, manufacturer, type, ip, additional_info, purchase, employee_id)
    
    def delete_asset(self, id, table):
        return self.model.delete_data(id, table)
    
    def validate_login(self, username):
        return self.model.validate_login(username)
    
    def successful_login(self, id):
        return self.model.successful_login(id)

    def update_software(self, id, sys_name, version, manufacturer):
        return self.model.edit_asset_software(id, sys_name, version, manufacturer)
    
    def link_assets(self, asset_hardware_id, asset_software_id):
        return self.model.link_assets(asset_hardware_id, asset_software_id)
    
    def find_vulnerabilities(self, asset_name):
        return self.model.find_vulnerabilities(asset_name)


