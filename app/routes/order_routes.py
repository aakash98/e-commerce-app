import json

from flask import request, jsonify
from app.utils import is_authenticated
from datetime import datetime, timedelta
from flask_jwt_extended import get_jwt_identity
from flask import Blueprint
from flask_jwt_extended import jwt_required
from app.utils.json_utils import jsonify_wrapper_mongo_engine
order_app = Blueprint('order_app', __name__)


@order_app.route('/order/place', methods=['POST'])
@jwt_required()
@is_authenticated
def place_order():
    from app.context.order import OrderContext
    data = request.json
    # try:
    context = OrderContext(**data)
    # except Exception as ex:
    #     return jsonify({'error': 'Order Creation Failed', 'exception': str(ex)}), 400
    if not context.dict().get('order', {}):
        return jsonify({'error': 'Order Creation Failed'}), 500
    order_data = context.dict().get('order', {})
    return jsonify({'data': order_data, 'success': True}), 200


@order_app.route('/order/id/<int:order_id>', methods=['GET'])
@jwt_required()
@is_authenticated
def get_by_id(order_id):
    from app.services import OrderService
    user = json.loads(get_jwt_identity())
    user_id = user['_id']
    order = OrderService.get_by_id(order_id, user_id)
    if order:
        return jsonify_wrapper_mongo_engine(order)
    else:
        return jsonify({'status': "Not Found"}), 404


@order_app.route('/order/user/<string:unit>/<int:quantity>')
@jwt_required()
def get_order_for_user_by_filters(unit, quantity):
    from app.services import OrderService
    user = json.loads(get_jwt_identity())
    user_id = user['_id']
    if unit == 'days' and quantity:
        since = datetime.now() - timedelta(days=quantity)
    else:
        since = None
    orders = OrderService.get_orders_for_users(user_id, since)
    return jsonify_wrapper_mongo_engine(orders)
