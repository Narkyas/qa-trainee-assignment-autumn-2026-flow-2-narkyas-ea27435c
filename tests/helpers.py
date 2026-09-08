def assert_status(response, expected_status, action):
    assert response.status_code == expected_status, (
        f"{action}: expected HTTP {expected_status}, "
        f"got {response.status_code}. "
        f"Response body: {response.text}"
    )