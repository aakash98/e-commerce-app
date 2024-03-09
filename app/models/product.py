import json

from mongoengine import (Document, StringField,
                         SequenceField, IntField, FloatField,
                         BooleanField, signals)

class Product(Document):
    id = SequenceField(primary_key=True)
    name = StringField(required=True)
    display_name = StringField(required=True)
    category = StringField(required=True)
    quantity = IntField(default=0)
    brand_name = StringField(required=True)
    brand_category = StringField(required=True)
    price = FloatField(required=True)
    is_active = BooleanField(default=True)

    @classmethod
    def post_save(cls, sender, document, **kwargs):
        from app.instance import move_to_es
        move_to_es.delay(json.loads(document.to_json()))
        print(f"Product {document.name} saved successfully")

signals.post_save.connect(Product.post_save, sender=Product)
