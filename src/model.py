import platform
import socket
import mysql.connector


class Model:
    # Global Variables
    db_config = {
        "host": "lochnagar.abertay.ac.uk",
        "user": "sql2301376",
        "password": "sweet angel friday nest",
        "database": "sql2301376",
    }

    # Constructor
    def __init__(self):
        # As soon as program is booted, get system information
        sys_name = platform.node()
        type = platform.system()
        model = platform.release()
        manufacturer = platform.machine()
        ip_address = socket.gethostbyname(socket.gethostname())

        all_assets = Model.get_all_assets()

        for asset in all_assets:
            if asset[1] == sys_name:
                break
            else:
                try:
                    conn = mysql.connector.connect(**Model.db_config)
                    curs = conn.cursor()

                    data = (sys_name, model, manufacturer, type, ip_address)
                    query = "INSERT INTO assets (`sys-name`, `model`, `manufacturer`, `type`, `ip-address`) VALUES (%s, %s, %s, %s, %s)"

                    curs.execute(query, data)
                    conn.commit()

                    print("Inserted Successfully")
                except mysql.connector.Error as e:
                    print("Failed to connect to database")

    # Close connection to database
    def close_connection(self, conn):
        conn.close()

    def get_all_assets(self):
        try:
            conn = mysql.connector.connect(**Model.db_config)
            curs = conn.cursor()

            curs.execute("SELECT * FROM assets")
            res = curs.fetchall()

            return res
        except mysql.connector.Error as e:
            print("Failed to connect to database")
            # Print error if connection to database fails
