from flask import Blueprint, request, jsonify
from models.cart_model import add_to_cart, get_cart, remove_from_cart
from utils.db import get_db_connection

cart_bp = Blueprint('cart', __name__)

# ADD TO CART (WITH VALIDATION)
@cart_bp.route('/cart/add', methods=['POST'])
def add_cart():
    data = request.json

    user_id = data['user_id']
    veg_id = data['veg_id']
    quantity = data['quantity']

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Get vegetable details
    cursor.execute("SELECT stock, max_limit FROM vegetables WHERE veg_id=%s", (veg_id,))
    veg = cursor.fetchone()

    if not veg:
        return jsonify({"message": "Vegetable not found"}), 404

    # 🚫 STOCK CHECK
    if quantity > veg['stock']:
        return jsonify({"message": f"Only {veg['stock']} available"}), 400

    # 🚫 THRESHOLD CHECK
    if quantity > veg['max_limit']:
        return jsonify({"message": f"Max limit is {veg['max_limit']}"}), 400

    # Add to cart
    add_to_cart(user_id, veg_id, quantity)

    return jsonify({"message": "Added to cart"}), 201


# GET CART
@cart_bp.route('/cart/<int:user_id>', methods=['GET'])
def view_cart(user_id):
    data = get_cart(user_id)
    return jsonify(data), 200


# REMOVE ITEM
@cart_bp.route('/cart/remove/<int:cart_id>', methods=['DELETE'])
def remove_item(cart_id):
    remove_from_cart(cart_id)
    return jsonify({"message": "Item removed"}), 200