from peewee import *
from db import db
from datetime import datetime

class User(Model):
    username = CharField(unique=True)
    hashed_password = CharField()
    role = CharField() # user, editor, admin

    class Meta:
        database = db
class Article(Model):
    title = CharField()
    content = TextField()
    author = ForeignKeyField(User, backref='articles')
    created_at = DateTimeField(default=datetime.utcnow)

    class Meta:
        database = db