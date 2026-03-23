from utils.db import get_db_connection

def create_user(name, phone, password, flat_no, role, building_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO users (name, phone, password, flat_no, role, building_id)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    
    cursor.execute(query, (name, phone, password, flat_no, role, building_id))
    conn.commit()

    cursor.close()
    conn.close()


def get_user_by_phone(phone):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT * FROM users WHERE phone = %s"
    cursor.execute(query, (phone,))
    
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    return user