import uuid
import requests

from helpers import assert_status
# Специально игнорируется fixtures user, token, item, чтобы проверить полный цикл объявления
BASE_URL = "https://qa-internship.avito.com"


def test_full_item_lifecycle():
    # 1. Регистрация
    username = f"student_{uuid.uuid4().hex[:8]}"
    password = "strong-password"

    register_response = requests.post(
        f"{BASE_URL}/api/1/register",
        json={
            "username": username,
            "password": password,
        },
    )

    assert_status(
        register_response,
        201,
        "Регистрация пользователя в E2E-сценарии"
    )


    user = register_response.json()

    assert "id" in user
    assert user["username"] == username

    seller_id = user["id"]

    # 2. Авторизация
    auth_response = requests.post(
        f"{BASE_URL}/api/1/autorize",
        json={
            "username": username,
            "password": password,
        },
    )

    assert_status(
        auth_response,
        200,
        "Авторизация пользователя в E2E-сценарии"
    )


    auth_data = auth_response.json()

    assert "accessToken" in auth_data
    assert auth_data["tokenType"] == "Bearer"

    headers = {
        "Authorization": f"Bearer {auth_data['accessToken']}",
        "Content-Type": "application/json",
    }

    # 3. Создание объявления
    item_payload = {
        "sellerID": seller_id,
        "name": f"testItem_{uuid.uuid4().hex[:8]}",
        "price": 9900,
        "statistics": {
            "likes": 21,
            "viewCount": 11,
            "contacts": 43,
        },
    }

    create_response = requests.post(
        f"{BASE_URL}/api/1/item",
        headers=headers,
        json=item_payload,
    )

    assert_status(
        create_response,
        200,
        "Создание объявления в E2E-сценарии"
    )

    create_data = create_response.json()
    assert "status" in create_data

    item_id = create_data["status"].split()[-1]

    # 4. Получение объявления
    get_response = requests.get(
        f"{BASE_URL}/api/1/item/{item_id}",
        headers=headers,
    )

    assert_status(
        get_response,
        200,
        f"Получение созданного объявления {item_id}"
    )

    item_data = get_response.json()

    assert len(item_data) == 1
    assert item_data[0]["id"] == item_id
    assert item_data[0]["sellerId"] == seller_id
    assert item_data[0]["name"] == item_payload["name"]
    assert item_data[0]["price"] == item_payload["price"]

    # 5. Получение объявлений продавца
    seller_items_response = requests.get(
        f"{BASE_URL}/api/1/{seller_id}/item",
        headers=headers,
    )

    assert_status(
        seller_items_response,
        200,
        f"Получение объявлений продавца {seller_id}"
    )
    seller_items = seller_items_response.json()

    assert any(product["id"] == item_id for product in seller_items)

    # 6. Получение статистики
    statistics_response = requests.get(
        f"{BASE_URL}/api/1/statistic/{item_id}",
        headers=headers,
    )
    assert_status(
        statistics_response,
        200,
        f"Получение статистики объявления {item_id}"
    )
   
    statistics = statistics_response.json()

    assert len(statistics) > 0
    assert statistics[0]["likes"] == 21
    assert statistics[0]["viewCount"] == 11
    assert statistics[0]["contacts"] == 43

    # 7. Удаление объявления
    delete_response = requests.delete(
        f"{BASE_URL}/api/2/item/{item_id}",
        headers=headers,
    )

    assert_status(
        delete_response,
        200,
        f"Удаление объявления {item_id}"
    )

    # 8. Проверка удаления
    final_response = requests.get(
        f"{BASE_URL}/api/1/item/{item_id}",
        headers=headers,
    )

    assert_status(
        final_response,
        404,
        f"Проверка удаления объявления {item_id}"
    )