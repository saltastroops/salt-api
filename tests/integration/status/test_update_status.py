from unittest.mock import patch, MagicMock

import fastapi
import pytest
from pytest import MonkeyPatch
from starlette import status
from starlette.testclient import TestClient


def _status_update():
    return {}


@pytest.mark.parametrize("ip", ["10.3.78.0", "145.16.9.9"])
def test_user_must_not_be_outside_local_network(ip: str, client: TestClient) -> None:
    request_client = MagicMock()
    request_client.host = ip
    with patch.object(fastapi.Request, "client", request_client):
        response = client.post("/status-update", json=_status_update())
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert "SAAO network" in response.json()["message"]


@pytest.mark.parametrize(
    "ip, status_code",
    [("10.1.0.34", status.HTTP_200_OK), ("10.2.99.8", status.HTTP_200_OK)],
)
def test_user_may_be_within_local_network(
    ip: str, status_code: int, client: TestClient
) -> None:
    request_client = MagicMock()
    request_client.host = ip
    with patch.object(fastapi.Request, "client", request_client):
        response = client.post("/status-update", json=_status_update())
        assert response.status_code == status.HTTP_200_OK


def test_status_update_is_created():
    assert False


def test_missing_subsystem():
    assert False


def test_missing_status():
    assert False


def test_missing_status_change_time():
    assert False


def test_status_change_time_not_necessary_for_same_status():
    assert False


def test_no_reason_required():
    assert False


def test_expected_eta_not_allowed_for_available_status():
    assert False


def test_reporting_user_missing():
    assert False
