import pytest
from django import urls


@pytest.mark.django_db
def test_login_200(api_client, superuser):
    res = api_client.post(
        urls.reverse("accounts:login"),
        {"username": "admin", "password": "admin"},
    )
    assert res.status_code == 200, res.data
