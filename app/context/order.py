from pydantic import BaseModel, model_validator, ValidationError
from typing import Dict, Optional, List, Union
from datetime import datetime
from app.services import OrderService
import json


class OrderContext(BaseModel):
    user_id: int
    address_name: str
    user: Dict
    address: Dict
    items: List[Dict]
    amount: float
    discounts: Optional[float] = 0.0
    payment: Optional[Dict]
    is_paid: Optional[bool] = False
    fulfilled_at: Optional[Union[datetime, None]] = None
    order: Optional[Dict] = None

    @classmethod
    def get_user_from_user_id(cls, user_id):
        from app.services import UserService
        if not user_id:
            raise ValidationError(f"UserID Missing")
        user = UserService.get_by_id(user_id)
        if not user:
            raise ValidationError(f"User Not Found")
        return json.loads(user.to_json())

    @classmethod
    def get_address_from_name(cls, address_name, addresses):
        if not address_name:
            raise ValidationError(f"Address Name Missing")
        for address in addresses:
            if address.get('name') == address_name:
                return address

    @classmethod
    def stage_items(cls, items):
        from app.services import ProductService
        amount = 0
        if not items:
            raise ValidationError(f"Items Missing")
        new_items = []
        for item in items:
            item_id = item.get('id')
            quantity = item.get('quantity', 1) or 1
            if not (item_id and quantity):
                raise ValidationError(f"Invalid Request For Item {item}")
            item_object = ProductService.get_by_id(item_id)
            if not item_object or not item_object.quantity or item_object.quantity < quantity:
                if not item_object or not item_object.quantity:
                    raise ValidationError(f"Item {item_id} Out Of Stock")
                raise ValidationError(f"Only {item_object.quantity} Items Are Left For {item_object.display_name}")
            item_amount = item_object.price * quantity
            amount += item_amount
            order_item = {'product': item_object, 'quantity': quantity, 'price': item_amount}
            new_items.append(order_item)
        return new_items, amount

    @classmethod
    def pre_validate_payment(cls, payment_info):
        # TODO: Implement Phase 1 Validation Of Cards/Validity/Digital Payment OTPs, etc
        return {'mode': 'cash'}

    @model_validator(mode='before')
    def validate_pre_order(cls, values):
        values['user'] = cls.get_user_from_user_id(values['user_id'])
        values['address'] = cls.get_address_from_name(values['address_name'], values['user']['addresses'])
        values['items'], values['amount'] = cls.stage_items(values['items'])
        values['payment'] = cls.pre_validate_payment({})
        return values

    @model_validator(mode='after')
    def validate_order_creation(cls, values):
        try:
            order_object = OrderService.create_order(values)
            values.order = json.loads(order_object.to_json())
        except Exception as ex:
            raise ValidationError(f"Order Creation Failed Due To {ex}")
        return
