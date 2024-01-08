import os
import subprocess
import socket
import mysql.connector
import re
from datetime import date


class Model:
    # Class Variables
    db_config = {
        "host": "lochnagar.abertay.ac.uk",
        "user": "sql2301376",
        "password": "sweet angel friday nest",
        "database": "sql2301376",
    }  

    # Gets all assets from database
    def get_all_assets(self, table):
        try:
            conn = mysql.connector.connect(**self.db_config)
            curs = conn.cursor()

            select_all_query = "SELECT * FROM %s"
            curs.execute(select_all_query, table)

            res = curs.fetchall()

            curs.close()
            conn.close()

            return res
        except mysql.connector.Error as e:
            return(e)
            # Print error if connection to database fails

    # Creates a new asset in the database
    def insert_asset(self, system_name, model, manufacturer, type, ip_address, additional_information, purchase_date, employee):
        try:
            conn = mysql.connector.connect(**Model.db_config)
            curs = conn.cursor()

            if not additional_information.strip():
                additional_information = None

            if not purchase_date.strip():
                purchase_date = None


            data = (system_name, model, manufacturer, type, ip_address, additional_information , purchase_date, employee[0])

            insert_query = "INSERT INTO assets(sys_name, model, manufacturer, type, ip_address, additional_information, purchase_date, employee_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"

            curs.execute(insert_query, data)
            conn.commit()

            return "Hardware Asset Added!"
        except mysql.connector.Error as e:
            return e
        
    def insert_asset_software(self, system_name, version, manufacturer):
        try:
            conn = mysql.connector.connect(**Model.db_config)
            curs = conn.cursor()

            data = (system_name, version, manufacturer)

            insert_query = "INSERT INTO assets_software (sys_name, version, manufacturer) VALUES (%s, %s, %s)"

            curs.execute(insert_query, data)
            conn.commit()

            return "Software Asset Added!"
        except mysql.connector.Error as e:
            return e

    # Gets an asset from the database by using it's ID
    def delete_data(self, asset, table):
        try:
            conn = mysql.connector.connect(**Model.db_config)
            curs = conn.cursor()

            id = (asset[0],)

            delete_query = "DELETE FROM %s WHERE id=%s"

            curs.execute(delete_query, table, id)
            conn.commit()

            return "Asset Deleted!"
        except mysql.connector.Error as e:
            return e

    # Gets an asset from the database by using it's ID
    def get_asset_by_id(self, asset, table):
        try:

            conn = mysql.connector.connect(**Model.db_config)
            curs = conn.cursor()

            asset_list = asset.split()
            id = (asset_list[0],)
            
            find_query = "SELECT * FROM %s WHERE id = %s"

            curs.execute(find_query, table, id)

            res = curs.fetchone()

            curs.close()
            conn.close()

            return res
        except mysql.connector.Error as e:
            return(e)

    # Edits an existing asset by using it's ID
    def edit_asset(self,id,system_name,model,manufacturer,type,ip_address,additional_info,purchase_date,employee_id):
        try:
            conn = mysql.connector.connect(**Model.db_config)
            curs = conn.cursor()

            data = (system_name, model, manufacturer, type, ip_address, additional_info, purchase_date, employee_id, id)

            edit_query = "UPDATE assets SET sys_name=%s, model=%s, manufacturer=%s, type=%s, ip_address=%s, additional_information=%s, purchase_date=%s, employee_id=%s WHERE id=%s"

            curs.execute(edit_query, data)
            conn.commit()

            return "Asset Edited Successfuly!"
        except mysql.connector.Error as e:
            return e
        
    def edit_asset_software(self,id,system_name,version,manufacturer):
        try:
            conn = mysql.connector.connect(**Model.db_config)
            curs = conn.cursor()

            data = (system_name,version,manufacturer,id)

            edit_query = "UPDATE assets_software SET sys_name=%s, version=%s, manufacturer=%s WHERE id=%s"

            curs.execute(edit_query, data)
            conn.commit()

            return "Software Asset Edited Successfuly!"
        except mysql.connector.Error as e:
            return e

    def add_employee(self, first_name, last_name, email, department):
        try:
            conn = mysql.connector.connect(**Model.db_config)
            curs = conn.cursor()

            data = (first_name, last_name, email, department)

            insert_query = "INSERT INTO employees (first_name, last_name, email_address, department) VALUES (%s, %s, %s, %s)"
        
            curs.execute(insert_query, data)
            conn.commit()

            return "Employee Added!"
        except mysql.connector.Error as e:
            return e

    def get_all_employees(self):
        try:
            conn = mysql.connector.connect(**Model.db_config)
            curs = conn.cursor()

            q = "SELECT * from employees"

            curs.execute(q)
            employees = curs.fetchall()

            curs.close()
            conn.close()

            return employees
        except mysql.connector.Error as e:
            return e
        
    def validate_login(self, username):
        try:
            conn = mysql.connector.connect(**Model.db_config)
            curs = conn.cursor()

            username = (username,)

            query = "SELECT * FROM employees WHERE email_address = %s"

            curs.execute(query, username)
            res = curs.fetchone()

            print(res)

            curs.close()
            conn.close()

            return res
        except mysql.connector.Error as e:
            return(e)
            # Print error if connection to database fails
        
        
    def successful_login(self, emp_id):
        # On a successful, get system information and adds to database if not already added
        # This does not include extra information or purchase date

        def get_hardware_info(emp_id):
            result = subprocess.run(['systeminfo'], capture_output=True, text=True)
            system_info = result.stdout

            # Funky Monkey code that gets the needed information from the 'systeminfo' command in terminal
            sys_name = re.search(r'Host Name:\s+(.*)', system_info).group(1).strip()
            model = re.search(r'System Model:\s+(.*)', system_info).group(1).strip()
            manufacturer = re.search(r'System Manufacturer:\s+(.*)', system_info).group(1).strip()
            type = re.search(r'System Type:\s+(.*)', system_info).group(1).strip()
            ip_address = socket.gethostbyname(socket.gethostname())

            hardware_info = (sys_name, model, manufacturer, type, ip_address, emp_id)

            print(hardware_info)
            
            return hardware_info

        def get_os_info():
            result = subprocess.run(['systeminfo'], capture_output=True, text=True)
            system_info = result.stdout

            # Same Funky Monkey code as before but this time it's for the software information
            sys_name = re.search(r'OS Name:\s+(.*)', system_info).group(1).strip()
            version = re.search(r'OS Version:\s+(.*)', system_info).group(1).strip()
            manufacturer = re.search(r'OS Manufacturer:\s+(.*)', system_info).group(1).strip()

            software_info = (sys_name, version, manufacturer)

            print(software_info)

            return software_info

        hardware_info = get_hardware_info(emp_id)
        software_info = get_os_info()

        try:
            conn = mysql.connector.connect(**Model.db_config)
            curs = conn.cursor()

            select_query_hardware = "SELECT * FROM assets WHERE sys_name = %s AND model = %s AND manufacturer = %s AND type = %s AND ip_address = %s AND employee_id = %s"
            insert_query_hardware = "INSERT INTO assets (sys_name, model, manufacturer, type, ip_address, employee_id) VALUES (%s, %s, %s, %s, %s, %s)"

            select_query_software = "SELECT * FROM assets_software WHERE sys_name = %s AND version = %s AND manufacturer = %s"
            insert_query_software = "INSERT INTO assets_software (sys_name, version, manufacturer) VALUES (%s, %s, %s)"

            # Checks if computer is in database
            curs.execute(select_query_hardware, hardware_info)
            this_computer_in_database = curs.fetchall()

            if not this_computer_in_database:
                curs.execute(insert_query_hardware, hardware_info)
                conn.commit()
                print("Hardware not in database - added successfully")
            else:
                print("Hardware already in database")

            curs.execute(select_query_software, software_info)
            this_software_in_database = curs.fetchall()

            if not this_software_in_database:
                curs.execute(insert_query_software, software_info)
                conn.commit()
                print("Software not in database - added successfully")
            else:
                print("Software already in database")

            curs.close()
            conn.close()

        except mysql.connector.Error as e:
            print(e)

    def link_assets(self, asset_hardware_id, asset_software_id):
        try:
            conn = mysql.connector.connect(**Model.db_config)
            curs = conn.cursor()

            data = (asset_hardware_id, asset_software_id, date.today())

            insert_query = "INSERT INTO assets_linked (hardware_id, software_id, date_linked) VALUES (%s, %s, %s)"

            curs.execute(insert_query, data)
            conn.commit()

            return "Assets Linked!"
        except mysql.connector.Error as e:
            return e


        
    