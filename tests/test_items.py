import uuid
import requests
from helpers import assert_status
BASE_URL = "https://qa-internship.avito.com"


def test_create_item_success(item):
    assert item["id"] is not None
    assert item["sellerID"] is not None
    assert item["name"] is not None
    assert item["price"] == 9900


def test_create_item_with_foreign_seller_id(user, auth_headers):
    payload = {
        "sellerID": user["id"] + 1,
        "name": "testItem",
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

    assert_status(
        response,
        400,
        "Создание объявления с чужим sellerID"
    )


def test_create_item_without_auth(user):
    payload = {
        "sellerID": user["id"],
        "name": "testItem",
        "price": 9900,
        "statistics": {
            "likes": 21,
            "viewCount": 11,
            "contacts": 43,
        },
    }

    response = requests.post(
        f"{BASE_URL}/api/1/item",
        json=payload,
    )

    assert_status(
        response,
        401,
        "Создание объявления без авторизации"
    )


def test_create_item_with_invalid_token(user):
    payload = {
        "sellerID": user["id"],
        "name": "testItem",
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
            "Authorization": "Bearer invalid-token",
            "Content-Type": "application/json",
        },
        json=payload,
    )
    assert_status(
        response,
        401,
        "Создание объявления с недействительным токеном"
    )

def test_get_item_success(item, auth_headers):
    response = requests.get(
        f"{BASE_URL}/api/1/item/{item['id']}",
        headers=auth_headers,
    )

    assert_status(
        response,
        200,
        f"Получение существующего объявления {item['id']}"
    )

    data = response.json()

    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["id"] == item["id"]
    assert data[0]["sellerId"] == item["sellerID"]
    assert data[0]["name"] == item["name"]
    assert data[0]["price"] == item["price"]


def test_get_nonexistent_item(auth_headers):
    fake_item_id = str(uuid.uuid4())

    response = requests.get(
        f"{BASE_URL}/api/1/item/{fake_item_id}",
        headers=auth_headers,
    )
    assert_status(
        response,
        404,
        f"Получение несуществующего объявления {fake_item_id}"
    )



def test_get_item_with_invalid_uuid(auth_headers):
    response = requests.get(
        f"{BASE_URL}/api/1/item/not-a-uuid",
        headers=auth_headers,
    )

    assert_status(
        response,
        400,
        "Получение объявления с некорректным UUID"
    )