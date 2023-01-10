from typing import Callable, Any

import pytest
from fastapi.testclient import TestClient
from starlette import status

# import saltapi.service.finder_chart_service
from saltapi.settings import Settings, get_settings
from tests.conftest import (
    authenticate,
    find_username,
    check_data,
)

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

