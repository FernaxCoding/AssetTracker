import platform
import socket
import mysql.connector

class Model:
    def __init__(self):
        # As soon as program is booted, get system information
        sys_name = platform.node()
        type = platform.system()
        model = platform.release()
        manufacturer = platform.machine()
        ip_address = socket.gethostbyname(socket.gethostname)
        
        cursor = connect()
        
        
    # Connect to database
    def connect():
        db_config = {
            "host": "lochnagar.abertay.ac.uk",
            "user": "sql2301376",
            "password": "sweet angel friday nest",
            "database": "sql2301376"
        }
        
        conn = mysql.connector.connect(**db_config)
        return conn
    
    # Close connection to database
    def close_connection(conn):
        conn.close()
        