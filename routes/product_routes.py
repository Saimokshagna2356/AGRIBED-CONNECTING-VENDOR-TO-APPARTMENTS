from flask import Blueprint, request, jsonify
from models.product_model import get_all_vegetables, add_vegetable

product_bp = Blueprint('products', __name__)

# GET ALL VEGETABLES
@product_bp.route('/vegetables', methods=['GET'])
def get_vegetables():
    data = get_all_vegetables()
    return jsonify(data), 200


# ADD VEGETABLE (ADMIN)
@product_bp.route('/admin/add-vegetable', methods=['POST'])
def add_product():
    data = request.json

    name = data['name']
    price = data['price']
    stock = data['stock']
    max_limit = data['max_limit']
    vendor_id = data['vendor_id']

    add_vegetable(name, price, stock, max_limit, vendor_id)

    return jsonify({"message": "Vegetable added"}), 201