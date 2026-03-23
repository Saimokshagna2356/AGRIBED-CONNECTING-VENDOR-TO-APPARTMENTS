from utils.db import get_db_connection

def get_all_vegetables():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM vegetables WHERE status = 'available'")
    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return data


def add_vegetable(name, price, stock, max_limit, vendor_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO vegetables (name, price, stock, max_limit, vendor_id)
    VALUES (%s, %s, %s, %s, %s)
    """

    cursor.execute(query, (name, price, stock, max_limit, vendor_id))
    conn.commit()

    cursor.close()
    conn.close()