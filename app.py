from flask import Flask
from routes.auth_routes import auth_bp
from routes.product_routes import product_bp   # 👈 ADD THIS
from routes.cart_routes import cart_bp
from routes.order_routes import order_bp

app = Flask(__name__)

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(product_bp)   # 👈 ADD THIS
app.register_blueprint(cart_bp)
app.register_blueprint(order_bp)

@app.route("/")
def home():
    return """
    <h1>🌱 Agribed</h1>
    <p>Connecting vegetable vendors to apartment residents.</p>
    <p>Backend API is running successfully.</p>
    """

if __name__ == "__main__":
    app.run(debug=True)