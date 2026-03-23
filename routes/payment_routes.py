from flask import Blueprint, request, jsonify
import razorpay
import os
import hmac
import hashlib
from utils.db import get_db_connection

payment_bp = Blueprint('payment', __name__)

# ===============================
# 🔑 RAZORPAY CLIENT
# ===============================
RAZORPAY_KEY_ID = "rzp_live_SUjlLO5E9MNmfV"
RAZORPAY_KEY_SECRET = "8Y1Yay4yBWzb5kHATk2VpTKu"

client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))


# ===============================
# 💳 CREATE PAYMENT ORDER
# ===============================
@payment_bp.route('/create-payment', methods=['POST'])
def create_payment():
    data = request.json

    amount = int(data['amount'] * 100)  # ₹ to paise
    user_id = data['user_id']

    try:
        payment = client.order.create({
            "amount": amount,
            "currency": "INR",
            "payment_capture": 1
        })

        return jsonify({
            "order_id": payment['id'],
            "amount": payment['amount'],
            "key": RAZORPAY_KEY_ID
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ===============================
# ✅ VERIFY PAYMENT (VERY IMPORTANT)
# ===============================
@payment_bp.route('/verify-payment', methods=['POST'])
def verify_payment():
    data = request.json

    razorpay_order_id = data['razorpay_order_id']
    razorpay_payment_id = data['razorpay_payment_id']
    razorpay_signature = data['razorpay_signature']

    # Generate signature
    generated_signature = hmac.new(
        RAZORPAY_KEY_SECRET.encode(),
        f"{razorpay_order_id}|{razorpay_payment_id}".encode(),
        hashlib.sha256
    ).hexdigest()

    if generated_signature == razorpay_signature:
        # Payment SUCCESS
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # Update order status
            cursor.execute("""
                UPDATE orders
                SET payment_status = 'paid'
                WHERE order_id = %s
            """, (data['order_id'],))

            conn.commit()
            cursor.close()
            conn.close()

            return jsonify({
                "message": "Payment verified successfully"
            }), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    else:
        return jsonify({
            "message": "Payment verification failed"
        }), 400