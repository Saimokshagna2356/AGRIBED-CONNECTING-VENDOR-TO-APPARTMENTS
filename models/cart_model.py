from utils.db import get_db_connection

def add_to_cart(user_id, veg_id, quantity):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Check existing item
    cursor.execute(
        "SELECT * FROM cart WHERE user_id=%s AND veg_id=%s",
        (user_id, veg_id)
    )
    item = cursor.fetchone()

    if item:
        # Update quantity
        new_qty = item['quantity'] + quantity
        cursor.execute(
            "UPDATE cart SET quantity=%s WHERE cart_id=%s",
            (new_qty, item['cart_id'])
        )
    else:
        # Insert new item
        cursor.execute(
            "INSERT INTO cart (user_id, veg_id, quantity) VALUES (%s, %s, %s)",
            (user_id, veg_id, quantity)
        )

    conn.commit()
    cursor.close()
    conn.close()


def get_cart(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
SELECT c.cart_id, c.veg_id, v.name, v.price, v.max_limit, v.stock, c.quantity
    FROM cart c
    JOIN vegetables v ON c.veg_id = v.veg_id
    WHERE c.user_id = %s
    """

    cursor.execute(query, (user_id,))
    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return data


def remove_from_cart(cart_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM cart WHERE cart_id=%s", (cart_id,))
    conn.commit()

    cursor.close()
    conn.close()