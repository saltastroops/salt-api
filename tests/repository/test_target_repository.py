from typing import Any

import pytest
from sqlalchemy.engine import Connection

from saltapi.repository.target_repository import TargetRepository
from tests.markers import nodatabase


@nodatabase
@pytest.mark.parametrize(
    "target_id",
    [
        35252,
        22186,
        36148,
        36136,
        35250,  # magnitude range
        34930,  # no coordinates
        # non-sidereal
        862,  # no Horizons target
        34931,  # Horizons target
        # proper motion
        35057,  # proper motion
        35170,  # no proper motion; target has a speed of 0 in right ascension and
        # declination
        36149,  # no proper motion defined
        # period ephemeris
        8960,  # period ephemeris
        36086,  # no period ephemeris
        # Horizons identifier
        34921,  # Horizons identifier
        35223,  # no Horizons identifier
    ],
)
def test_coordinates(
    target_id: int, db_connection: Connection, check_data: Any
) -> None:
    target_repository = TargetRepository(db_connection)
    target = target_repository.get(target_id)
    check_data(target)
