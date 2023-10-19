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

    # Constructor
    def __init__(self):
        # As soon as program is booted, get system information and adds to database if not already added
        # This does not include extra information or purchase date
        sys_name = platform.node()
        type = platform.system()
        model = platform.release()
        manufacturer = platform.machine()
        ip_address = socket.gethostbyname(socket.gethostname())

        this_computer = (sys_name, model, manufacturer, type, ip_address)

        try:
            conn = mysql.connector.connect(**self.db_config)
            curs = conn.cursor()

            select_query = "SELECT * FROM assets WHERE `sys-name` = %s AND `model` = %s AND manufacturer = %s AND type = %s AND `ip-address` = %s"
            insert_query = "INSERT INTO assets (`sys-name`, `model`, `manufacturer`, `type`, `ip-address`) VALUES (%s, %s, %s, %s, %s)"

            # Checks if computer is in database
            curs.execute(select_query, this_computer)
            this_computer_in_database = curs.fetchall()

            if not this_computer_in_database:
                curs.execute(insert_query, this_computer)
                conn.commit()
                print("Computer not in database - added successfully")
                curs.close()
                conn.close()
            else:
                print("Computer already in database")
                curs.close()
                conn.close()
        except mysql.connector.Error as e:
            print(e)

    # Gets all assets from database
    def get_all_assets(self):
        try:
            conn = mysql.connector.connect(**self.db_config)
            curs = conn.cursor()

            select_all_query = "SELECT * FROM assets"
            curs.execute(select_all_query)

            res = curs.fetchall()

            # for row in res:
            #     print(row)

            curs.close()
            conn.close()

            return res
        except mysql.connector.Error as e:
            print(e)
            # Print error if connection to database fails

    # Creates a new asset in the database
    def insert_asset(
        self,
        system_name,
        model,
        manufacturer,
        type,
        ip_address,
        additional_info,
        purchase_date,
    ):
        try:
            conn = mysql.connector.connect(**Model.db_config)
            curs = conn.cursor()

            data = (
                system_name,
                model,
                manufacturer,
                type,
                ip_address,
                additional_info,
                purchase_date,
            )
            insert_query = "INSERT INTO `assets` (`sys-name`, `model`, `manufacturer`, `type`, `ip-address`, `additional-info`, `purchase-date`) VALUES (%s, %s, %s, %s, %s, %s, %s, )"

            curs.execute(insert_query, data)
            conn.commit()

            print("Asset Added")
        except mysql.connector.Error as e:
            print(e)

    # Gets an asset from the database by using it's ID
    def delete_data(self, id):
        try:
            conn = mysql.connector.connect(**Model.db_config)
            curs = conn.cursor()

            delete_query = "DELETE FROM assets WHERE id=%s"

            curs.execute(delete_query, id)
            conn.commit()

            print("Asset Deleted")
        except mysql.connector.Error as e:
            print(e)

    # Gets an asset from the database by using it's ID
    def get_asset_by_id(self, id):
        try:
            conn = mysql.connector.connect(**Model.db_config)
            curs = conn.cursor()

            find_query = "SELECT * FROM assets WHERE id=%s"

            curs.execute(find_query, id)
            conn.commit()

            res = curs.fetchone()

            return res
        except mysql.connector.Error as e:
            print(e)

    # Edits an existing asset by using it's ID
    def edit_asset(
        self,
        id,
        system_name,
        model,
        manufacturer,
        type,
        ip_address,
        additional_info,
        purchase_date,
    ):
        try:
            conn = mysql.connector.connect(**Model.db_config)
            curs = conn.cursor()

            data = (
                system_name,
                model,
                manufacturer,
                type,
                ip_address,
                additional_info,
                purchase_date,
                id,
            )

            edit_query = "UPDATE assets SET `sys-name`=%s, `model`=%s, `manufacturer`=%s, `type`=%s, `ip-address`=%s, `additional-info`=%s, `purchase-date`=%s WHERE id=%s"

            curs.execute(edit_query, data)
            conn.commit()

            print("Asset Edited")
        except mysql.connector.Error as e:
            print(e)
