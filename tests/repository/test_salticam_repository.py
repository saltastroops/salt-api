from typing import Any

import pytest
from sqlalchemy.engine import Connection

from saltapi.repository.salticam_repository import SalticamRepository


@pytest.mark.parametrize(
    "salticam_id",
    [
        393,
        # Detector windows
        1043,  # no detector windows
        590,  # three detector windows; used in block with id 6602
        887,  # detector window with different width and height; used in block with id
        # 23352
        # Procedure
        1215,  # multiple filters; used in block with id 89445
    ],
)
def test_salticam(salticam_id: int, db_connection: Connection, check_data: Any) -> None:
    salticam_repository = SalticamRepository(db_connection)
    salticam = salticam_repository.get(salticam_id)
    check_data(salticam)
