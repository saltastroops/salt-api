import uuid
from datetime import datetime, timedelta
from typing import Dict
from unittest.mock import MagicMock, patch

import fastapi
import pytest
from starlette import status
from starlette.testclient import TestClient


def _default_status_update() -> Dict[str, str]:
    status_changed_at = datetime.utcnow().replace(microsecond=0)
    expected_available_again_at = status_changed_at + timedelta(days=1)

    return dict(
        expected_available_again_at=expected_available_again_at.isoformat() + "+00:00",
        reason=str(uuid.uuid4()),
        reporting_user=str(uuid.uuid4()),
        status="Unavailable",
        status_changed_at=status_changed_at.isoformat() + "+00:00",
        subsystem="RSS",
    )


@pytest.mark.parametrize("ip", ["10.3.78.0", "145.16.9.9"])
def test_user_must_not_be_outside_local_network(ip: str, client: TestClient) -> None:
    # The status can only be updated from within the SAAO network.
    request_client = MagicMock()
    request_client.host = ip
    with patch.object(fastapi.Request, "client", request_client):
        response = client.patch("/status", json=_default_status_update())
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert "SAAO network" in response.json()["message"]


@pytest.mark.parametrize(
    "ip, status_code",
    [("10.1.0.34", status.HTTP_200_OK), ("10.2.99.8", status.HTTP_200_OK)],
)
def test_user_may_be_within_local_network(
    ip: str, status_code: int, saao_client: TestClient
) -> None:
    # The status can be updated from within the SAAO network.
    response = saao_client.patch("/status", json=_default_status_update())
    assert response.status_code == status.HTTP_200_OK


def test_status_is_updated(saao_client: TestClient):
    # The status is updated successfully when calling the /status endpoint.
    status_update = _default_status_update()
    response = saao_client.patch("/status", json=status_update)
    assert response.status_code == status.HTTP_200_OK

    # Update the status and check the returned value
    updated_status = response.json()
    assert len(updated_status) > 1  # multiple subsystems are returned
    updated_subsystem_status = [
        s for s in updated_status if s["subsystem"] == status_update["subsystem"]
    ][0]
    assert response.status_code == status.HTTP_200_OK
    assert updated_subsystem_status == status_update


def test_missing_subsystem(saao_client: TestClient):
    # A missing subsystem leads to a 422 error.
    status_update = _default_status_update()
    status_update["subsystem"] = None  # type: ignore

    response = saao_client.patch("/status", json=status_update)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "subsystem" in response.json()["message"]


def test_missing_status(saao_client: TestClient):
    # A missing status leads to a 422 error.

    status_update = _default_status_update()
    status_update["subsystem"] = None  # type: ignore

    response = saao_client.patch("/status", json=status_update)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "subsystem" in response.json()["message"]


def test_reporting_user_missing(saao_client: TestClient):
    # A missing reporting user leads to a 422 error.

    status_update = _default_status_update()
    status_update["reporting_user"] = None  # type: ignore

    response = saao_client.patch("/status", json=status_update)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "reporting_user" in response.json()["message"]


def test_missing_status_change_time(saao_client: TestClient):
    # A missing status leads to a 400 error.

    # Ensure we start with an unavailable subsystem.
    status_update = _default_status_update()
    status_update["status"] = "Unavailable"
    response = saao_client.patch("/status", json=status_update)
    assert response.status_code == status.HTTP_200_OK

    # Now make another update, but for another status
    new_status_update = _default_status_update()
    new_status_update["status"] = "Available with restrictions"
    new_status_update["status_changed_at"] = None  # type: ignore

    response = saao_client.patch("/status", json=new_status_update)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_expected_available_not_allowed_for_available_status(
    saao_client: TestClient,
) -> None:
    # No expected time for availability again must be supplied if the subsystem is
    # available.
    status_update = _default_status_update()
    status_update["status"] = "Available"
    response = saao_client.patch("/status", json=status_update)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "expected" in response.json()["message"]


@pytest.mark.parametrize("timeshift", [timedelta(seconds=0), timedelta(seconds=1)])
def test_expected_available_must_be_later_than_status_change(
    timeshift: timedelta, saao_client: TestClient
) -> None:
    # The expected time when the subsystem is available again must be later than the
    # time when the status changed.
    status_update = _default_status_update()
    expected_available_again_at = datetime.utcnow()
    status_changed_at = expected_available_again_at + timeshift
    status_update["status_changed_at"] = status_changed_at.isoformat() + "+00:00"
    status_update["expected_available_again_at"] = (
        expected_available_again_at.isoformat() + "+00:00"
    )

    response = saao_client.patch("/status", json=status_update)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "later" in response.json()["message"]


def test_previous_values_are_reused(saao_client: TestClient):
    # If the status change time, expected time of availability again or reason are not
    # supplied and the status remains the same, their current values are reused.

    # Ensure we start with a known status
    status_update = _default_status_update()
    status_update["status"] = "Unavailable"
    response = saao_client.patch("/status", json=status_update)
    assert response.status_code == status.HTTP_200_OK

    # Update the status
    new_status_update = _default_status_update()
    new_status_update["status"] = status_update["status"]
    new_status_update["status_changed_at"] = None  # type: ignore
    new_status_update["expected_available_again_at"] = None  # type: ignore
    new_status_update["reason"] = None  # type: ignore
    response = saao_client.patch("/status", json=new_status_update)
    assert response.status_code == status.HTTP_200_OK

    # Get the new status
    response = saao_client.get("/status")
    final_status = [
        s for s in response.json() if s["subsystem"] == new_status_update["subsystem"]
    ][0]
    assert final_status["status_changed_at"] == status_update["status_changed_at"]
    assert (
        final_status["expected_available_again_at"]
        == status_update["expected_available_again_at"]
    )
    assert final_status["reason"] == status_update["reason"]
