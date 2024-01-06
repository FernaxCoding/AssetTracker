import platform
import socket
import mysql.connector


class Model:
    # Class Variables
    db_config = {
        "host": "lochnagar.abertay.ac.uk",
        "user": "sql2301376",
        "password": "sweet angel friday nest",
        "database": "sql2301376",
    }  

    # Gets all assets from database
    def get_all_assets(self):
        try:
            conn = mysql.connector.connect(**self.db_config)
            curs = conn.cursor()

            select_all_query = "SELECT * FROM assets"
            curs.execute(select_all_query)

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

            return "Asset Added!"
        except mysql.connector.Error as e:
            return e

    # Gets an asset from the database by using it's ID
    def delete_data(self, asset):
        try:
            conn = mysql.connector.connect(**Model.db_config)
            curs = conn.cursor()

            id = (asset[0],)

            delete_query = "DELETE FROM assets WHERE id=%s"

            curs.execute(delete_query, id)
            conn.commit()

            return "Asset Deleted!"
        except mysql.connector.Error as e:
            return e

    # Gets an asset from the database by using it's ID
    def get_asset_by_id(self, asset):
        try:

            conn = mysql.connector.connect(**Model.db_config)
            curs = conn.cursor()

            asset_list = asset.split()
            id = (asset_list[0],)
            
            find_query = "SELECT * FROM assets WHERE id = %s"

            curs.execute(find_query, id)

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

        sys_name = platform.node()
        type = platform.system()
        model = platform.release()
        manufacturer = platform.machine()
        ip_address = socket.gethostbyname(socket.gethostname())

        this_computer = (sys_name, model, manufacturer, type, ip_address, emp_id)

        try:
            conn = mysql.connector.connect(**Model.db_config)
            curs = conn.cursor()

            select_query = "SELECT * FROM assets WHERE sys_name = %s AND model = %s AND manufacturer = %s AND type = %s AND ip_address = %s AND employee_id = %s"
            insert_query = "INSERT INTO assets (sys_name, model, manufacturer, type, ip_address) VALUES (%s, %s, %s, %s, %s, %s)"

            # Checks if computer is in database
            curs.execute(select_query, this_computer)
            this_computer_in_database = curs.fetchall()

            if not this_computer_in_database:
                curs.execute(insert_query, this_computer)
                conn.commit()
                print("Computer not in database - added successfully")
            else:
                print("Computer already in database")
            curs.close()
            conn.close()
        except mysql.connector.Error as e:
            print(e)
    