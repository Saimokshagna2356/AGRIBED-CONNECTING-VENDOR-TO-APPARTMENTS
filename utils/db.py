import mysql.connector
from config import Config

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="agribed"
        )
        return connection

    except Exception as e:
        print("DB not connected:", e)
        return None