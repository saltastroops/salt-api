from typing import Any, Callable

import pytest
from sqlalchemy.engine import Connection

from saltapi.repository.hrs_repository import HrsRepository


@pytest.mark.parametrize(
    "hrs_id",
    [
        639,  # no overhead time
        1350,  # in block with id 87924
        261,  # nod and shuffle; in block with id 31270
        1615,  # ThAr lamp in; in block with id 73634
        2319,  # high resolution
        2298,  # high stability
        2320,  # low resolution
        2327,  # medium resolution
        244,  # the sky fiber is placed on the optical axis
        2328,  # the star fiber is placed on the optical axis
        1829,  # the star and sky fiber are equidistant from the optical axis
        2297,  # iodine cell in
        2320,  # iodine cell out
        1615,  # ThAr in sky fiber
        2316,  # one amplifier; used in block with id 89472
        80,  # multiple amplifiers; different pre-binned rows and columns; used in block
        # with id 24956
        385,  # used in block with id 33293
    ],
)
def test_hrs(
    db_connection: Connection, check_data: Callable[[Any], None], hrs_id: int
) -> None:
    hrs_repository = HrsRepository(db_connection)
    hrs = hrs_repository.get(hrs_id)
    check_data(hrs)
