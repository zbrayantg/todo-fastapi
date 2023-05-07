from fastapi.testclient import TestClient

from app.main import app


def create_user_and_make_login(username: str):
    client = TestClient(app)

    user = {
        "email": f"{username}@example.com",
        "username": username,
        "password": "strongpass123",
    }

    response = client.post(
        "/api/v1/user/",
        json=user,
    )

    login = {"username": username, "password": "strongpass123"}

    response = client.post(
        "/api/v1/login/",
        data=login,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        follow_redirects=True,
    )

    data = response.json()
    return data["access_token"]


def test_create_todo_ok():
    token = create_user_and_make_login("test_create_todo_ok")

    client = TestClient(app)

    todo = {"title": "My first task"}

    response = client.post(
        "/api/v1/todo/",
        json=todo,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["title"] == todo["title"]
    assert data["is_done"] is False
