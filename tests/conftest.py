import uuid #для генерации
import pytest
import requests

BASE_URL = "https://qa-internship.avito.com"

@pytest.fixture
def user():
    username = f"student_{uuid.uuid4().hex[:8]}"
    password = "strong-password"

    response = requests.post(
        f"{BASE_URL}/api/1/register",
        json={
            "username": username,
            "password": password,
        },
    )

    assert response.status_code == 201, (
        f"Registration failed: {response.status_code}, "
        f"body: {response.text}"
    )

    data = response.json()

    assert "id" in data
    assert "username" in data

    return {
        "id": data["id"],
        "username": data["username"],
        "password": password,
    }


@pytest.fixture
def token(user):
    response = requests.post(
        f"{BASE_URL}/api/1/autorize",
        json={
            "username": user["username"],
            "password": user["password"],
        },
    )

    assert response.status_code == 200, (
        f"Authorization failed: {response.status_code}, "
        f"body: {response.text}"
    )

    data = response.json()

    assert "accessToken" in data
    assert data.get("tokenType") == "Bearer"

    return data["accessToken"]


@pytest.fixture
def auth_headers(token):
    return {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
    }


@pytest.fixture
def item(user, auth_headers):
    payload = {
        "sellerID": user["id"],
        "name": f"testItem_{uuid.uuid4().hex[:8]}",
        "price": 9900,
        "statistics": {
            "likes": 21,
            "viewCount": 11,
            "contacts": 43,
        },
    }

    response = requests.post(
        f"{BASE_URL}/api/1/item",
        headers={
            **auth_headers,
            "Content-Type": "application/json",
        },
        json=payload,
    )

    assert response.status_code == 200, (
        f"Item creation failed: {response.status_code}, "
        f"body: {response.text}"
    )

    data = response.json()

    assert "status" in data

    status = str(data["status"])
    # UUID находится внутри строки status.
    parts = status.split()
    item_id = parts[-1]

    # Проверяем, что UUID действительно корректный.
    uuid.UUID(item_id)
    item_data = {
        "id": item_id,
        "sellerID": user["id"],
        "name": payload["name"],
        "price": payload["price"],
        "statistics": payload["statistics"],
    }

    yield item_data

    # Cleanup: удаляем объявление после теста
    delete_response = requests.delete(
        f"{BASE_URL}/api/2/item/{item_id}",
        headers=auth_headers,
    )

    assert delete_response.status_code in (200, 404), (
        f"Cleanup failed: {delete_response.status_code}, "
        f"body: {delete_response.text}"
    )

@pytest.fixture
def item_for_delete(user, auth_headers):
    payload = {
        "sellerID": user["id"],
        "name": f"testItem_{uuid.uuid4().hex[:8]}",
        "price": 9900,
        "statistics": {
            "likes": 21,
            "viewCount": 11,
            "contacts": 43,
        },
    }

    response = requests.post(
        f"{BASE_URL}/api/1/item",
        headers={**auth_headers, "Content-Type": "application/json"},
        json=payload,
    )

    assert response.status_code == 200, (
        f"Item creation failed: {response.status_code}, "
        f"body: {response.text}"
    )

    data = response.json()
    assert "status" in data

    item_id = str(data["status"]).split()[-1]
    uuid.UUID(item_id)

    return {
        "id": item_id,
        "sellerID": user["id"],
        "name": payload["name"],
        "price": payload["price"],
        "statistics": payload["statistics"],
    }
