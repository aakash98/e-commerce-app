from app.models import Order, User
from datetime import datetime, timedelta
class OrderService:

    @classmethod
    def create_order(cls, order_context):
        product_collector = []
        for order_item in order_context.items:
            product = order_item['product']
            product.quantity -= order_item['quantity']
            if product.quantity < 0:
                raise Exception(f"{product.display_name} Out Of Stock")
            product_collector.append(product)
        for product in product_collector:
            product.save()
        order = Order(user_id=order_context.user['_id'],
                      address=order_context.address,
                      amount=order_context.amount,
                      discounts=0.0,
                      items=order_context.items,
                      payment=order_context.payment,
                      is_paid=False)
        order.save()
        return order

    @classmethod
    def get_by_id(cls, order_id, user_id):
        user = User.objects(id=user_id).first()
        if user and (user.is_staff or user.is_superuser):
            order = Order.objects(id=order_id).first()
        elif user:
            order = Order.objects(id=order_id, user=user).first()
        else:
            order = None
        return order

    @classmethod
    def get_orders_for_users(cls, user_id, since=None):
        user = User.objects(id=user_id).first()
        if not user:
            raise Exception(f"User Not Found {user_id}")
        if not since:
            since = datetime.now() - timedelta(days=7)
        orders = Order.objects(user_id=user_id, created_at__gte=since)
        return orders
