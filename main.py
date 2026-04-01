from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from creating_tables import User, Article
from auth import verify_password, create_token, decode_token
from schemas import ArticleCreate, ArticleUpdate, ArticleResponse, UserUpdate

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

@app.on_event("startup")
def startup():
    database = User._meta.database
    if database.is_closed():
        database.connect()
    database.create_tables([User, Article], safe=True)

@app.on_event("shutdown")
def shutdown():
    database = User._meta.database
    if not database.is_closed():
        database.close()

@app.get("/health")
def health():
    return {"status":"staying alive"}
#auth system
@app.post("/auth/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = User.get_or_none(User.username == form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    token = create_token(user.id, user.role)
    return {"access_token": token, "token_type": "bearer"}
def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = User.get_or_none(User.id == int(payload["sub"]))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
#articles
@app.get("/articles")
def get_articles(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    search: str = Query(None),
    current_user: User = Depends(get_current_user)
):
    query = Article.select()
    if search:
        query = query.where(
            Article.title.contains(search) | Article.content.contains(search)
        )
    articles = query.limit(limit).offset(offset)
    return [
        {"id": a.id, "title": a.title, "content": a.content,
         "author_id": a.author_id, "created_at": a.created_at}
        for a in articles
    ]
@app.get("/articles/{article_id}")
def get_article(article_id: int, current_user: User = Depends(get_current_user)):
    article = Article.get_or_none(Article.id == article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return {"id": article.id, "title": article.title, "content": article.content,
            "author_id": article.author_id, "created_at": article.created_at}

@app.post("/articles", status_code=201)
def create_article(data: ArticleCreate, current_user: User = Depends(get_current_user)):
    article = Article.create(
        title = data.title,
        content = data.content,
        author = current_user.id,
    )
    return {"id": article.id, "title": article.title, "content": article.content,
            "author_id": article.author_id, "created_at": article.created_at}

@app.put("/articles/{article_id}")
def update_article(article_id: int, data: ArticleUpdate, current_user: User = Depends(get_current_user)):
    article = Article.get_or_none(Article.id == article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    #user can only modify their articles
    if current_user.role == "user" and article.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="You are not allowed to modify")

    if data.title:
        article.title = data.title
    if data.content:
        article.content = data.content
    article.save()
    return {"id": article.id, "title": article.title, "content": article.content,
            "author_id": article.author_id, "created_at": article.created_at}
@app.delete("/articles/{article_id}", status_code=204)
def delete_article(article_id: int, current_user: User = Depends(get_current_user)):
    article = Article.get_or_none(Article.id == article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    if current_user.role == "user" and article.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed")
    if current_user.role == "editor":
        raise HTTPException(status_code=403, detail="Editors cannot delete articles")

    article.delete_instance()
    return
#users
@app.get("/users")
def get_users(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    search: str = Query(None),
    current_user: User = Depends(get_current_user)
):
    query = User.select()
    if search:
        query = query.where(User.username.contains(search))
    users = query.limit(limit).offset(offset)
    return [
        {"id": u.id, "username": u.username, "role": u.role}
        for u in users
    ]

@app.get("/users/{user_id}")
def get_user(user_id: int, current_user: User = Depends(get_current_user)):
    user = User.get_or_none(User.id == user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": user.id, "username": user.username, "role": user.role}

@app.put("/users/{user_id}")
def update_user(user_id: int, data: UserUpdate, current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admins can update users")
    user = User.get_or_none(User.id == user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if data.role:
        user.role = data.role
    if data.username:
        user.username = data.username
    user.save()
    return {"id": user.id, "username": user.username, "role": user.role}

@app.delete("/users/{user_id}", status_code=204)
def delete_user(user_id: int, current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admins can delete users")
    user = User.get_or_none(User.id == user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.delete_instance()
    return