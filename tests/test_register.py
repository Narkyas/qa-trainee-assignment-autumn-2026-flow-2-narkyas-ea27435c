import requests
from helpers import assert_status
BASE_URL = "https://qa-internship.avito.com"


def test_register_success(user):
    assert user["id"] is not None
    assert user["username"].startswith("student_")


def test_register_empty_username():
    response = requests.post(
        f"{BASE_URL}/api/1/register",
        json={
            "username": "",
            "password": "strong-password",
        },
    )

    assert_status(
        response,
        400,
        "Регистрация с пустым username"
    )


def test_register_empty_password():
    response = requests.post(
        f"{BASE_URL}/api/1/register",
        json={
            "username": "student_test_empty_password",
            "password": "",
        },
    )

    assert_status(
        response,
        400,
        "Регистрация с пустым password"
    )