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
except:
    print("DB not connected")
        return None