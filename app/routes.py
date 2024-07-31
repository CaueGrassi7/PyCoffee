from flask import request, jsonify, Blueprint
from . import db
from .models import Product

bp = Blueprint('catalog', __name__)

def validate_product_data(data):
    if 'name' not in data or not isinstance(data['name'], str) or not data['name'].strip():
        return 'Invalid or missing "name" field'
    if 'description' not in data or not isinstance(data['description'], str) or not data['description'].strip():
        return 'Invalid or missing "description" field'
    if 'price' not in data or not isinstance(data['price'], (int, float)) or data['price'] <= 0:
        return 'Invalid or missing "price" field. Must be a positive number'
    return None

@bp.route('/products', methods=['POST'])
def add_product():
    data = request.get_json()

    error_message = validate_product_data(data)
    if error_message:
        return jsonify({'error': error_message}), 400

    new_product = Product(name=data['name'], description=data['description'], price=data['price'])
    db.session.add(new_product)
    db.session.commit()
    return jsonify(new_product.to_dict()), 201

@bp.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([product.to_dict() for product in products])

@bp.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    product = Product.query.get(id)
    if product is None:
        return jsonify({'error': 'Product not found'}), 404
    return jsonify(product.to_dict())

@bp.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
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
