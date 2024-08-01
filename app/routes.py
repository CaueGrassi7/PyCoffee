from flask import request, jsonify, Blueprint, flash, redirect, url_for
from . import db
from .models import Product, Order, order_product, User
from flask_login import login_user, logout_user, login_required, current_user

bp = Blueprint('catalog', __name__)

# Product Routes
def validate_product_data(data):
    if 'name' not in data or not isinstance(data['name'], str) or not data['name'].strip():
        return 'Invalid or missing "name" field'
    if 'description' not in data or not isinstance(data['description'], str) or not data['description'].strip():
        return 'Invalid or missing "description" field'
    if 'price' not in data or not isinstance(data['price'], (int, float)) or data['price'] <= 0:
        return 'Invalid or missing "price" field. Must be a positive number'
    return None

@bp.route('/products', methods=['POST'])
@login_required
def add_product():
    if not current_user.is_admin():
        return jsonify({'error': 'Unauthorized'}), 403

    data = request.get_json()
    error_message = validate_product_data(data)
    if error_message:
        return jsonify({'error': error_message}), 400

    new_product = Product(name=data['name'], description=data['description'], price=data['price'])
    db.session.add(new_product)
    db.session.commit()
    return jsonify(new_product.to_dict()), 201

@bp.route('/products', methods=['GET'])
@login_required
def get_products():
    products = Product.query.all()
    return jsonify([product.to_dict() for product in products])

@bp.route('/products/<int:id>', methods=['GET'])
@login_required
def get_product(id):
    product = Product.query.get(id)
    if product is None:
        return jsonify({'error': 'Product not found'}), 404
    return jsonify(product.to_dict())

@bp.route('/products/<int:id>', methods=['PUT'])
@login_required
def update_product(id):
    if not current_user.is_admin():
        return jsonify({'error': 'Unauthorized'}), 403

    product = Product.query.get_or_404(id)
    data = request.get_json()

    error_message = validate_product_data(data)
    if error_message:
        return jsonify({'error': error_message}), 400

    if 'name' in data:
        product.name = data['name']
    if 'description' in data:
        product.description = data['description']
    if 'price' in data:
        product.price = data['price']

    db.session.commit()
    return jsonify(product.to_dict())

@bp.route('/products/<int:id>', methods=['DELETE'])
@login_required
def delete_product(id):
    if not current_user.is_admin():
        return jsonify({'error': 'Unauthorized'}), 403

    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({'message': 'Product deleted successfully'}), 200

# Order Routes
@bp.route('/orders', methods=['POST'])
@login_required
def create_order():
    data = request.get_json()
    product_quantities = data['products']
    
    new_order = Order()
    db.session.add(new_order)
    db.session.flush()  # Para obter o ID do pedido antes de commit

    total_price = 0.0
    for pq in product_quantities:
        product = Product.query.get_or_404(pq['product_id'])
        quantity = pq['quantity']
        db.session.execute(order_product.insert().values(order_id=new_order.id, product_id=product.id, quantity=quantity))
        total_price += product.price * quantity

    new_order.total_price = total_price
    db.session.commit()
    return jsonify(new_order.to_dict()), 201

@bp.route('/orders/<int:order_id>', methods=['PUT'])
@login_required
def update_order_status(order_id):
    data = request.get_json()
    new_status = data.get('status')
    
    order = Order.query.get_or_404(order_id)
    order.status = new_status
    db.session.commit()
    
    return jsonify(order.to_dict()), 200

# User Routes
@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({'error': 'Missing required fields'}), 400

    user = User(username=username, email=email, role='client')
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'Registration successful!'}), 201

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Missing email or password'}), 400

    user = User.query.filter_by(email=email).first()
    if user is None or not user.check_password(password):
        return jsonify({'error': 'Invalid email or password'}), 401

    login_user(user)
    return jsonify({'message': 'Login successful!'}), 200

@bp.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logout successful!'}), 200

@bp.route('/admin', methods=['GET'])
@login_required
def admin():
    if not current_user.is_admin():
        return jsonify({'error': 'You do not have permission to access this page.'}), 403
    return jsonify({'message': 'Welcome to the admin page!'})

@bp.route('/', methods=['GET'])
@login_required
def index():
    return jsonify({'message': 'Welcome to the index page!'})
