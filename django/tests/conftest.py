import pytest
from rest_framework.test import APIClient

from tests.factories import accounts


@pytest.fixture
def api_client():
    api = APIClient()
    return api


@pytest.fixture
def superuser():
    return accounts.superuser()
