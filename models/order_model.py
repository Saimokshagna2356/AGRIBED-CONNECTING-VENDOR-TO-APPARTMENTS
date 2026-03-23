from utils.db import get_db_connection

def create_order(user_id, total_price, payment_method, delivery_slot):
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO orders (user_id, total_price, payment_method, delivery_slot)
    VALUES (%s, %s, %s, %s)
    """

    cursor.execute(query, (user_id, total_price, payment_method, delivery_slot))
    conn.commit()

    order_id = cursor.lastrowid

    cursor.close()
    conn.close()

    return order_id


def add_order_items(order_id, items):
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO order_items (order_id, veg_id, quantity, price)
    VALUES (%s, %s, %s, %s)
    """

    for item in items:
        cursor.execute(query, (
            order_id,
            item['veg_id'],
            item['quantity'],
            item['price']
        ))

    conn.commit()
    cursor.close()
    conn.close()


def clear_cart(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM cart WHERE user_id=%s", (user_id,))
    conn.commit()

    cursor.close()
    conn.close()