from typing import Any

import pytest
from sqlalchemy.engine import Connection

from saltapi.repository.bvit_repository import BvitRepository


@pytest.mark.parametrize("bvit_id", [34, 75])
def test_bvit(bvit_id: int, db_connection: Connection, check_data: Any) -> None:
    bvit_repository = BvitRepository(db_connection)
    bvit = bvit_repository.get(bvit_id)
    check_data(bvit)
