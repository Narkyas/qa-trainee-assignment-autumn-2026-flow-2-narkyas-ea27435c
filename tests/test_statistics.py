import requests

from helpers import assert_status
BASE_URL = "https://qa-internship.avito.com"


def test_get_statistics_v1_success(item, auth_headers):
    response = requests.get(
        f"{BASE_URL}/api/1/statistic/{item['id']}",
        headers=auth_headers,
    )
    assert_status(
        response,
        200,
        f"Получение статистики v1 для объявления {item['id']}"
    )

    data = response.json()

    assert isinstance(data, list)
    assert len(data) > 0


def test_get_statistics_v2_success(item, auth_headers):
    response = requests.get(
        f"{BASE_URL}/api/2/statistic/{item['id']}",
        headers=auth_headers,
    )

    assert_status(
        response,
        200,
        f"Получение статистики v2 для объявления {item['id']}"
    )

    data = response.json()

    assert isinstance(data, list)
    assert len(data) > 0


def test_statistics_match_item_data(item, auth_headers):
    response = requests.get(
        f"{BASE_URL}/api/1/statistic/{item['id']}",
        headers=auth_headers,
    )

    assert_status(
        response,
        200,
        f"Проверка соответствия статистики данным объявления {item['id']}"
    )

    data = response.json()

    statistics = data[0]

    assert statistics["likes"] == item["statistics"]["likes"]
    assert statistics["viewCount"] == item["statistics"]["viewCount"]
    assert statistics["contacts"] == item["statistics"]["contacts"]


def test_statistics_nonexistent_item(auth_headers):
    fake_item_id = "550e8400-e29b-41d4-a716-446655440000"

    response = requests.get(
        f"{BASE_URL}/api/1/statistic/{fake_item_id}",
        headers=auth_headers,
    )

    assert_status(
        response,
        404,
        f"Получение статистики несуществующего объявления {fake_item_id}"
    )


def test_statistics_without_auth(item):
    response = requests.get(
        f"{BASE_URL}/api/1/statistic/{item['id']}",
    )

    assert_status(
        response,
        401,
        f"Получение статистики без авторизации для объявления {item['id']}"
    )