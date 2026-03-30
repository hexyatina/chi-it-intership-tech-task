from peewee import *
from db import db
from creating_tables import User, Article
from auth import hash_password
password = ["admin_pass", "editor_pass", "user_pass"]

db.connect()
admin = User.create(username ="ortem", hashed_password = hash_password(password[0][:72]), role = "admin")
editor = User.create(username="editor", hashed_password=hash_password(password[1][:72]), role = "editor")
user = User.create(username="user", hashed_password=hash_password(password[2][:72]), role = "user")
total = [admin, editor, user]
for u in total:
    print(f"created {u.username}, role: {u.role}")
db.close()