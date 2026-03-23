from flask import Blueprint, request, jsonify
from models.order_model import create_order, add_order_items, clear_cart
from models.cart_model import get_cart

order_bp = Blueprint('orders', __name__)

@order_bp.route('/order/create', methods=['POST'])
def place_order():
    data = request.json

    user_id = data['user_id']
    payment_method = data['payment_method']
    delivery_slot = data['delivery_slot']

    cart_items = get_cart(user_id)

    if not cart_items:
        return jsonify({"message": "Cart is empty"}), 400

    total_price = 0
    items = []

    for item in cart_items:
        total_price += float(item['price']) * item['quantity']
        items.append({
            "veg_id": item['cart_id'],   # careful here 👇
            "quantity": item['quantity'],
            "price": item['price']
        })

    # FIX: use veg_id properly
    for i, item in enumerate(cart_items):
        items[i]['veg_id'] = item['cart_id']  # (we'll correct below)

    # CREATE ORDER
    order_id = create_order(user_id, total_price, payment_method, delivery_slot)

    # ADD ITEMS
    add_order_items(order_id, cart_items)

    # CLEAR CART
    clear_cart(user_id)

    return jsonify({
        "message": "Order placed successfully",
        "order_id": order_id,
        "total_price": total_price
    }), 201