from datetime import datetime
from entity.Role import Role
from flask_mongoengine import Document
from mongoengine import StringField, DateTimeField, ListField, IntField, EnumField

class AccountIdentity(Document):
    # _id由mongodb自动生成，因此这里不要定义_id，否则不会自动生成_id的值
    # _id = IntField(primary_key=True)
    account = StringField(unique=True)
    password = StringField()
    role = EnumField(Role)
    timestamp = DateTimeField(default=datetime.now)
    trueName = StringField()
    email = StringField()
    phone = StringField()
    status = StringField()
    note = StringField()