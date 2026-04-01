
from db import db
from creating_tables import User, Article
from auth import hash_password
password = ["admin_pass", "editor_pass", "user_pass"]

db.connect()

db.create_tables([User, Article], safe=True) #double checking because it may cause troubles on docker
Article.delete().execute()
User.delete().execute()
print("Cleared existing data")


admin = User.create(username ="ortem", hashed_password = hash_password(password[0][:72]), role = "admin")
editor = User.create(username="editor", hashed_password=hash_password(password[1][:72]), role = "editor")
user = User.create(username="user", hashed_password=hash_password(password[2][:72]), role = "user")
total = [admin, editor, user]
for u in total:
    print(f"created {u.username}, role: {u.role}")

articles_data = [
    {"title": "Admin test", "content":"this article was written by admin", "author": admin},
    {"title": "Editor test", "content":"this article was written by editor", "author": editor},
    {"title": "User test", "content":"this article was written by user", "author": user}
]
for data in articles_data:
    article = Article.create(
        title=data["title"],
        content=data["content"],
        author=data["author"]
    )
    print(f"Created article: '{article.title}' by {data['author'].username}")
db.close()