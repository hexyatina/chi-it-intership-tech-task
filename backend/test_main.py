import pytest
from fastapi.testclient import TestClient
from peewee import SqliteDatabase
from creating_tables import User, Article
from backend.routers.auth import hash_password

TEST_DB_PATH = "test.db"
test_db = SqliteDatabase(TEST_DB_PATH)
User._meta.database = test_db
Article._meta.database = test_db

from main import app

@pytest.fixture(autouse=True)
def setup_db():
    if test_db.is_closed():
        test_db.connect()
    test_db.create_tables([User, Article], safe=True)

    User.create(username="admin", hashed_password=hash_password("admin_pass"), role="admin")
    User.create(username="editor", hashed_password=hash_password("editor_pass"), role="editor")
    User.create(username="user", hashed_password=hash_password("user_pass"), role="user")

    yield

    test_db.drop_tables([User, Article])
    if not test_db.is_closed():
        test_db.close()

@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c

def get_token(client, username: str, password: str):
    response = client.post("/auth/login", data={
        "username": username,
        "password": password
    })
    return response.json()["access_token"]

def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200

def test_login_success(client):
    response = client.post("/auth/login", data={"username": "admin", "password": "admin_pass"})
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_wrong_password(client):
    response = client.post("/auth/login", data={"username": "admin", "password": "wrong"})
    assert response.status_code == 400

def test_login_wrong_username(client):
    response = client.post("/auth/login", data={"username": "nobody", "password": "admin_pass"})
    assert response.status_code == 400

def test_get_articles_unauthorized(client):
    response = client.get("/articles")
    assert response.status_code == 401

def test_get_articles(client):
    token = get_token(client, "user", "user_pass")
    response = client.get("/articles", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200

def test_create_article(client):
    token = get_token(client, "user", "user_pass")
    response = client.post("/articles", json={"title": "Test", "content": "Content"}, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 201

def test_get_article_by_id(client):
    token = get_token(client, "user", "user_pass")
    create = client.post("/articles", json={"title": "Test", "content": "Content"}, headers={"Authorization": f"Bearer {token}"})
    article_id = create.json()["id"]
    response = client.get(f"/articles/{article_id}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200

def test_get_article_not_found(client):
    token = get_token(client, "user", "user_pass")
    response = client.get("/articles/999", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 404

def test_update_own_article(client):
    token = get_token(client, "user", "user_pass")
    create = client.post("/articles", json={"title": "Old", "content": "Old"}, headers={"Authorization": f"Bearer {token}"})
    article_id = create.json()["id"]
    response = client.put(f"/articles/{article_id}", json={"title": "New"}, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200

def test_update_other_article_as_user(client):
    admin_token = get_token(client, "admin", "admin_pass")
    user_token = get_token(client, "user", "user_pass")
    create = client.post("/articles", json={"title": "Admin article", "content": "content"}, headers={"Authorization": f"Bearer {admin_token}"})
    article_id = create.json()["id"]
    response = client.put(f"/articles/{article_id}", json={"title": "Hacked"}, headers={"Authorization": f"Bearer {user_token}"})
    assert response.status_code == 403

def test_delete_own_article(client):
    token = get_token(client, "user", "user_pass")
    create = client.post("/articles", json={"title": "To delete", "content": "content"}, headers={"Authorization": f"Bearer {token}"})
    article_id = create.json()["id"]
    response = client.delete(f"/articles/{article_id}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 204

def test_editor_cannot_delete(client):
    admin_token = get_token(client, "admin", "admin_pass")
    editor_token = get_token(client, "editor", "editor_pass")
    create = client.post("/articles", json={"title": "Article", "content": "content"}, headers={"Authorization": f"Bearer {admin_token}"})
    article_id = create.json()["id"]
    response = client.delete(f"/articles/{article_id}", headers={"Authorization": f"Bearer {editor_token}"})
    assert response.status_code == 403

def test_get_users(client):
    token = get_token(client, "user", "user_pass")
    response = client.get("/users", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200

def test_get_user_by_id(client):
    token = get_token(client, "admin", "admin_pass")
    response = client.get("/users/1", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200

def test_delete_user_as_admin(client):
    token = get_token(client, "admin", "admin_pass")
    response = client.delete("/users/3", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 204

def test_delete_user_as_non_admin(client):
    token = get_token(client, "user", "user_pass")
    response = client.delete("/users/1", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403