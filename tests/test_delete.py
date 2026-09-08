import requests
import uuid
from helpers import assert_status
BASE_URL = "https://qa-internship.avito.com"


def test_delete_item_success(item_for_delete, auth_headers):
    response = requests.delete(
        f"{BASE_URL}/api/2/item/{item_for_delete['id']}",
        headers=auth_headers,
    )

    assert response.status_code == 200


def test_get_item_after_delete(item_for_delete, auth_headers):
    delete_response = requests.delete(
        f"{BASE_URL}/api/2/item/{item_for_delete['id']}",
        headers=auth_headers,
    )
    assert_status(
        delete_response,
        200,
        f"Удаление объявления {item_for_delete['id']}"
    )
    assert delete_response.status_code == 200

    get_response = requests.get(
        f"{BASE_URL}/api/1/item/{item_for_delete['id']}",
        headers=auth_headers,
    )

    assert_status(
        get_response,
        404,
        f"Получение удалённого объявления {item_for_delete['id']}"
    )


def test_delete_item_twice(item_for_delete, auth_headers):
    first_response = requests.delete(
        f"{BASE_URL}/api/2/item/{item_for_delete['id']}",
        headers=auth_headers,
    )
    assert_status(
        first_response,
        200,
        f"Удаление объявления перед проверкой удаления {item_for_delete['id']}"
    )

    second_response = requests.delete(
        f"{BASE_URL}/api/2/item/{item_for_delete['id']}",
        headers=auth_headers,
    )

    assert_status(
        second_response,
        404,
        f"Повторное удаление объявления {item_for_delete['id']}"
    )


def test_delete_nonexistent_item(auth_headers):
    fake_item_id = str(uuid.uuid4())

    response = requests.delete(
        f"{BASE_URL}/api/2/item/{fake_item_id}",
        headers=auth_headers,
    )

    assert_status(
        response,
        404,
        f"Удаление несуществующего объявления {fake_item_id}"
    )

def test_delete_item_without_auth(item_for_delete, auth_headers):
    response = requests.delete(
        f"{BASE_URL}/api/2/item/{item_for_delete['id']}",
    )

    assert_status(
        response,
        401,
        f"Удаление объявления без авторизации {item_for_delete['id']}"
    )

    # После проверки 401 удаляем объявление авторизованным запросом,
    # чтобы не оставлять тестовые данные на стенде.
    cleanup_response = requests.delete(
        f"{BASE_URL}/api/2/item/{item_for_delete['id']}",
        headers=auth_headers,
    )

    assert_status(
        cleanup_response,
        200,
        f"Очистка тестового объявления {item_for_delete['id']}"
    )