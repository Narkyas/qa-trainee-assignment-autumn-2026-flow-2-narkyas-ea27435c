import requests
from helpers import assert_status
BASE_URL = "https://qa-internship.avito.com"


def test_get_seller_items_success(user, item, auth_headers):
    response = requests.get(
        f"{BASE_URL}/api/1/{user['id']}/item",
        headers=auth_headers,
    )

    assert_status(
        response,
        200,
        f"Получение объявлений продавца {user['id']}"
    )

    data = response.json()

    assert isinstance(data, list)
    assert any(product["id"] == item["id"] for product in data)


def test_get_seller_items_without_auth(user):
    response = requests.get(
        f"{BASE_URL}/api/1/{user['id']}/item",
    )
    assert_status(
        response,
        401,
        f"Получение объявлений продавца {user['id']} без авторизации"
    )


def test_get_seller_items_for_new_seller(user, auth_headers):
    response = requests.get(
        f"{BASE_URL}/api/1/{user['id']}/item",
        headers=auth_headers,
    )

    assert_status(
        response,
        200,
        f"Получение объявлений нового продавца {user['id']}"
    )


    data = response.json()
    assert isinstance(data, list)
    assert data == []