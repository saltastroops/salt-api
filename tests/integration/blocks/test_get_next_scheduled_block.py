from typing import Any, Callable, Optional

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.engine import Connection
from starlette import status

import saltapi.service.block_service
from saltapi.service.block import Block
from tests.conftest import authenticate, find_username, not_authenticated

BLOCKS_URL = "/blocks"

BLOCK = {
    "id": 1,
    "name": "BLOCK",
    "observation_probabilities": {
        "average_ranking": None,
        "competition": None,
        "moon": None,
        "observability": None,
        "seeing": None,
        "total": None,
    },
    "observation_time": 28664,
    "observations": [
        {
            "finder_charts": [
                {
                    "comment": None,
                    "files": [],
                    "id": 1124,
                    "valid_from": None,
                    "valid_until": None,
                }
            ],
            "observation_time": 28664,
            "overhead_time": 912,
            "phase_constraints": None,
            "target": {
                "id": 1,
                "name": "Target with id",
                "coordinates": None,
                "proper_motion": None,
                "magnitude": None,
                "target_type": None,
                "period_ephemeris": None,
                "horizons_identifier": None,
                "non_sidereal": False

            },
            "telescope_configurations": [
                {
                    "dither_pattern": None,
                    "guide_star": None,
                    "iterations": 1,
                    "use_parallactic_angle": False,
                    "payload_configurations": [
                        {
                            "calibration_filter": None,
                            "guide_method": "None",
                            "instruments": {
                                "bvit": None,
                                "hrs": None,
                                "rss": None,
                                "nir": None,
                                "salticam": None
                            },
                            "lamp": None,
                            "payload_configuration_type": "Acquisition",
                            "use_calibration_screen": False
                        }
                    ],
                    "position_angle": None,
                    "grating_angle": 0
                }
            ],
            "time_restrictions": None
        }
    ],
    "observing_conditions": {
        "maximum_lunar_phase": 15.0,
        "maximum_seeing": 2.5,
        "minimum_lunar_distance": 0.0,
        "minimum_seeing": 0.6,
        "transparency": "Clear"
    },
    "observing_windows": [],
    "overhead_time": 912,
    "priority": 0,
    "proposal_code": "2099-1-RSA-001",
    "ranking": None,
    "rejected_observations": 1,
    "requested_observations": 1,
    "semester": "2099-1",
    "comment": "",
    "code": None,
    "block_visits": [],
    "accepted_observations": 0,
    "status": {
        "value": "Active",
        "reason": None,
    },
    "wait_period": 3
}


def _mock_get_next_scheduled_block(db_connection: Connection) -> Callable[[str], Optional[Block]]:
    def f(*args: Any, **kwargs: Any) -> Optional[Block]:
        return BLOCK
    return f


def test_get_next_scheduled_block_requires_authentication(
        client: TestClient,
) -> None:
    not_authenticated(client)
    response = client.get(BLOCKS_URL + "/next-scheduled-block")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.parametrize(
    "username",
    [
        find_username("Investigator", proposal_code="2016-1-COM-001"),
        find_username("Principal Contact", proposal_code="2016-1-COM-001"),
        find_username("Principal Investigator", proposal_code="2016-1-COM-001"),
        find_username("TAC Member", partner_code="POL"),
        find_username("TAC Chair", partner_code="POL"),
        find_username("Board Member"),
    ],
)
def test_get_next_scheduled_block_requires_permissions(
        username: str, client: TestClient
) -> None:
    authenticate(username, client)
    response = client.get(BLOCKS_URL + "/next-scheduled-block")
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.parametrize(
    "username",
    [
        find_username("SALT Astronomer"),
        find_username("SALT Operator"),
        find_username("Administrator"),
    ],
)
def test_get_next_scheduled_block(
        db_connection: Connection,
        username: str,
        client: TestClient,
        monkeypatch: pytest.MonkeyPatch,
        check_data: Callable[[Any], None]
) -> None:
    authenticate(username, client)

    monkeypatch.setattr(
        saltapi.service.block_service.BlockService,
        "get_next_scheduled_block",
        _mock_get_next_scheduled_block(db_connection),
    )

    response = client.get(BLOCKS_URL + "/next-scheduled-block")

    assert response.status_code == status.HTTP_200_OK
    check_data(response.json())
