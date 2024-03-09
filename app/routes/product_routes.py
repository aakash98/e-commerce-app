from flask import request, jsonify
from app.services import ProductService
from app.utils import is_staff, is_superuser
from app.instance.cache import cache
from flask_jwt_extended import jwt_required
from flask import Blueprint
from app.utils.json_utils import jsonify_wrapper_mongo_engine
product_app = Blueprint('product_app', __name__)


@product_app.route('/products', methods=['GET'])
@cache.cached(timeout=60)
def get_products():
    products = ProductService.get_all_products()
    return jsonify_wrapper_mongo_engine(products)


@product_app.route('/products', methods=['POST'])
@jwt_required()
@is_staff
def create_product():
    data = request.json
    data = ProductService.create_new_product(data)
    return jsonify_wrapper_mongo_engine(data), 201


@product_app.route('/products/<int:product_id>', methods=['GET'])
@cache.cached(timeout=60)
def get_product(product_id):
    product = ProductService.get_by_id(product_id)
    if product:
        return jsonify_wrapper_mongo_engine(product), 200
    return jsonify({'error': 'Product not found'}), 404


@product_app.route('/products/<int:product_id>', methods=['PUT'])
@jwt_required()
@is_staff
def update_product(product_id):
    data = request.json
    result, _ok = ProductService.update_product(product_id, **data)
    if _ok:
        return jsonify_wrapper_mongo_engine(result), 200
    return jsonify({'error': 'Product not found'}), 404


@product_app.route('/products/<int:product_id>', methods=['DELETE'])
@jwt_required()
@is_superuser
def delete_product(product_id):
    _ok = ProductService.delete_product(product_id)
    if _ok:
        return jsonify({'success': 'True'}), 200
    return jsonify({'error': 'Product not found'}), 404
