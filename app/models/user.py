from mongoengine import IntField, Document, EmbeddedDocument, SequenceField, BooleanField, StringField, \
    EmbeddedDocumentListField


class Address(EmbeddedDocument):
    name = StringField(required=True)
    poc_name = StringField(required=True)
    poc_contact_number = StringField(required=True)
    line_1 = StringField(required=True)
    line_2 = StringField()
    pin_code = IntField(required=True)
    city = StringField(required=True)
    state = StringField(required=True)
    country = StringField(default='in')


class User(Document):
    id = SequenceField(primary_key=True)
    username = StringField(required=True)
    password = StringField(required=True)
    email = StringField(required=True)
    contact_number = StringField()
    addresses = EmbeddedDocumentListField(Address)
    is_staff = BooleanField(default=False)
    is_superuser = BooleanField(default=False)
