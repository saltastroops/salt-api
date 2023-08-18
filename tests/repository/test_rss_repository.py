from typing import Any, Callable

import pytest
from sqlalchemy.engine import Connection

from saltapi.repository.rss_repository import RssRepository
from tests.markers import nodatabase


@pytest.mark.parametrize(
    "rss_id",
    [
        24293,
        13543,  # no slit mask
        # Configurations
        20792,  # imaging
        23573,  # polarimetric imaging
        23472,  # spectroscopy
        20708,  # spectropolarimetry
        24087,  # MOS
        23231,  # MOS polarimetry
        17823,  # Fabry-Perot
        # Detector calculations
        20936,  # FP Ring Radius
        23225,  # MOS Acquisition
        24398,  # MOS Mask Calibration
        24223,  # No detector calculation
        # Procedures
        17823,  # Fabry-Perot
        24176,  # Polarimetry
        23286,  # Polarimetry
        # Arc bible entries
        18294,  # Ne and Xe
    ],
)
@nodatabase
def test_rss(
    rss_id: int, db_connection: Connection, check_data: Callable[[Any], None]
) -> None:
    rss_repository = RssRepository(db_connection)
    rss = rss_repository.get(rss_id)
    # Don't include the information whether the mask is in the magazine, as this changes
    # over time
    if rss["configuration"].get("mask") is not None:
        del rss["configuration"]["mask"]["is_in_magazine"]
    check_data(rss)
