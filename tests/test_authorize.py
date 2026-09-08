import requests
from helpers import assert_status

BASE_URL = "https://qa-internship.avito.com"


def test_authorize_success(user, token):
    assert token is not None
    assert len(token) > 0


def test_authorize_wrong_password(user):
    response = requests.post(
        f"{BASE_URL}/api/1/autorize",
        json={
            "username": user["username"],
            "password": "wrong-password",
        },
    )

    assert_status(
        response,
        401,
        "Авторизация с неверным паролем"
    )


def test_authorize_nonexistent_user():
    response = requests.post(
        f"{BASE_URL}/api/1/autorize",
        json={
            "username": "student_nonexistent_user_123456",
            "password": "strong-password",
        },
    )
    assert_status(
        response,
        401,
        "Авторизация несуществующего пользователя"
    )


def test_authorize_empty_username():
    response = requests.post(
        f"{BASE_URL}/api/1/autorize",
        json={
            "username": "",
            "password": "strong-password",
        },
    )

    assert_status(
        response,
        400,
        "Авторизация с пустым username"
    )