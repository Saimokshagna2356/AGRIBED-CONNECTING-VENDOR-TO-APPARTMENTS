import mysql.connector

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
        print("Database connection error:", e)
        return None