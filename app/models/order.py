from mongoengine import (EmbeddedDocument, Document, StringField, ReferenceField, ListField,
                         EmbeddedDocumentField, EmbeddedDocumentListField, SequenceField, FloatField, BooleanField,
                         IntField, DateTimeField)
from .user import User, Address
from .product import Product
from datetime import datetime, timedelta
import string
import random


def payment_id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


class Payment(EmbeddedDocument):
    id = StringField(default=payment_id_generator())
    mode = StringField(default='cash')
    created_at = DateTimeField(default=datetime.now)
    status = StringField(default='pending')


class OrderItem(EmbeddedDocument):
    product = ReferenceField(Product)
    quantity = IntField(default=1)
    price = FloatField(required=True)
    estimated_delivery_time = DateTimeField(default=datetime.now() + timedelta(days=10))
    delivered = BooleanField(default=False)


class Order(Document):
    id = SequenceField(primary_key=True)
    created_at = DateTimeField(default=datetime.now)
    user_id = IntField(required=True)
    address = EmbeddedDocumentField(Address)
    amount = FloatField(required=True)
    discounts = FloatField(required=True)
    items = EmbeddedDocumentListField(OrderItem)
    payment = EmbeddedDocumentField(Payment)
    is_paid = BooleanField(default=False)
    fulfilled_at = DateTimeField()
