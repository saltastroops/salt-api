from typing import Any, Callable

import pytest
from fastapi.testclient import TestClient
from starlette import status

from saltapi.settings import Settings, get_settings
from tests.conftest import authenticate, check_data, find_username

INSTITUTION_URL = "/institutions"


def test_create_institution(
        client: TestClient, check_data: Callable[[Any], None]
) -> None:
    institution = {
        "institution_name": "World University",
        "department": "Physics",
        "address": "1 Earth Street\nEarth\n0000",
        "url": "www.world-university.com",
    }
    response = client.post(INSTITUTION_URL + "/", json=institution)

    assert response.status_code == status.HTTP_201_CREATED
    check_data(response.json())

