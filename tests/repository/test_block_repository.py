from typing import Any, cast

import pytest
from sqlalchemy.engine import Connection
from sqlalchemy.exc import NoResultFound

from saltapi.exceptions import NotFoundError
from saltapi.repository.block_repository import BlockRepository
from saltapi.repository.instrument_repository import InstrumentRepository
from saltapi.repository.target_repository import TargetRepository
from saltapi.service.instrument import BVIT, HRS, RSS, Salticam
from saltapi.service.target import Target
from tests.markers import nodatabase


class FakeTargetRepository:
    def get(self, target_id: int) -> Target:
        return f"Target with id {target_id}"


class FakeInstrumentRepository:
    def get_salticam(self, salticam_id: int) -> Salticam:
        return f"Salticam with id {salticam_id}"

    def get_rss(self, rss_id: int) -> RSS:
        return f"RSS with id {rss_id}"

    def get_hrs(self, hrs_id: int) -> HRS:
        return f"HRS with id {hrs_id}"

    def get_bvit(self, bvit_id: int) -> BVIT:
        return f"BVIT with id {bvit_id}"


def create_block_repository(connection: Connection) -> BlockRepository:
    return BlockRepository(
        target_repository=cast(TargetRepository, FakeTargetRepository()),
        instrument_repository=cast(InstrumentRepository, FakeInstrumentRepository()),
        connection=connection,
    )


@nodatabase
@pytest.mark.parametrize(
    "block_id",
    [
        79390,  # general block content, accepted and rejected block visits
        89175,  # observing windows
        88649,  # target
        75444,  # finder charts without comments
        75551,  # finder charts with and without comments
        87431,  # finder charts with validity range
        88042,  # time restrictions
        69787,  # phase constraints
        89403,  # no time restrictions, no phase constraints
        89463,  # telescope configuration with position angle
        89382,  # telescope configuration without position angle
        89445,  # telescope configurations with and without dither pattern
        89204,  # guide star
        89480,  # no guide star
        89326,  # payload configurations with acquisition, science and calibration
        89444,  # two telescope configurations with two payload configurations; Salticam
        # and RSS
        76620,  # one telescope configuration with two payload configurations; Salticam
        # and HRS
        73735,  # one telescope configuration with two payload configuration and one
        # telescope configuration with one payload configuration; Salticam and BVIT
        1023,  # two telescope configurations with one payload configuration; multiple
        # instrument setups in payload configuration; Salticam
    ],
)
def test_get_block(block_id: int, db_connection: Connection, check_data: Any) -> None:
    block_repository = create_block_repository(db_connection)
    block = block_repository.get(block_id)
    check_data(block)


@nodatabase
@pytest.mark.parametrize(
    "block_id",
    [
        9005,  # subblock iterations
        9495,  # two observations in a pointing
    ],
)
def test_get_raises_error_for_too_complicated_blocks(
    block_id: int, db_connection: Connection
) -> None:
    # Blocks with multiple observations or with subblocks or subsubblocks should cause
    # an error

    block_repository = create_block_repository(db_connection)
    with pytest.raises(ValueError) as excinfo:
        block_repository.get(block_id)
    assert "supported" in str(excinfo)


@nodatabase
def test_get_raises_error_for_non_existing_block(db_connection: Connection) -> None:
    block_repository = create_block_repository(db_connection)
    with pytest.raises(NoResultFound):
        block_repository.get(1234567)


@nodatabase
@pytest.mark.parametrize(
    "block_id",
    [
        2339,  # block expired
        1,  # block on hold, block in queue
    ],
)
def test_get_block_status(
    block_id: int, db_connection: Connection, check_data: Any
) -> None:
    block_repository = create_block_repository(db_connection)
    status = block_repository.get_block_status(block_id)
    check_data(status)


@nodatabase
def test_get_block_status_raises_error_for_wrong_block_id(
    db_connection: Connection,
) -> None:
    block_repository = create_block_repository(db_connection)
    with pytest.raises(NoResultFound):
        block_repository.get_block_status(0)


@nodatabase
def test_update_block_status(db_connection: Connection) -> None:
    # Set the status to "On Hold" and the reason to "not needed"
    block_repository = create_block_repository(db_connection)
    block_id = 2339
    block_repository.update_block_status(block_id, "On hold", "not needed")
    block_status = block_repository.get_block_status(block_id)
    assert block_status["value"] == "On hold"
    assert block_status["reason"] == "not needed"

    # Now set it the status to "Active" and reason to "Awaiting driftscan"
    block_repository.update_block_status(block_id, "Active", "Awaiting driftscan")
    block_status = block_repository.get_block_status(block_id)
    assert block_status["value"] == "Active"
    assert block_status["reason"] == "Awaiting driftscan"


@nodatabase
def test_update_block_status_raises_error_for_wrong_block_id(
    db_connection: Connection,
) -> None:
    block_repository = create_block_repository(db_connection)
    with pytest.raises(NotFoundError):
        block_repository.update_block_status(0, "Active", "")


@nodatabase
def test_update_block_status_raises_error_for_wrong_status(
    db_connection: Connection,
) -> None:
    block_repository = create_block_repository(db_connection)
    with pytest.raises(ValueError) as excinfo:
        block_repository.update_block_status(1, "Wrong block status", "")

    assert "block status" in str(excinfo.value)


@nodatabase
@pytest.mark.parametrize(
    "block_visit_id",
    [
        5479,  # accepted block visit
        5457,  # rejected block visit
        1,  # block in queue
    ],
)
def test_get_block_visit(
    block_visit_id: int, db_connection: Connection, check_data: Any
) -> None:
    block_repository = create_block_repository(db_connection)
    block_visit = block_repository.get_block_visit(block_visit_id)
    check_data(block_visit)


@nodatabase
def test_get_block_visit_status_raises_error_for_wrong_block_visit_id(
    db_connection: Connection,
) -> None:
    block_repository = create_block_repository(db_connection)
    with pytest.raises(NotFoundError):
        block_repository.get_block_visit(0)


@nodatabase
def test_get_block_visit_raises_error_for_deleted_status(
    db_connection: Connection,
) -> None:
    block_repository = create_block_repository(db_connection)
    with pytest.raises(NotFoundError):
        block_repository.get_block_visit(829)


@nodatabase
def test_update_block_visit_status(db_connection: Connection) -> None:
    # Set the status to "Accepted"
    block_repository = create_block_repository(db_connection)
    block_visit_id = 2300  # The status for this block visit is "In queue"
    block_repository.update_block_visit_status(block_visit_id, "Accepted", None)
    block_visit = block_repository.get_block_visit(block_visit_id)
    assert block_visit["status"] == "Accepted"
    assert block_visit["rejection_reason"] is None

    # Now set it to "Rejected"
    block_repository.update_block_visit_status(block_visit_id, "Rejected", None)
    block_visit = block_repository.get_block_visit(block_visit_id)
    assert block_visit["status"] == "Rejected"
    assert block_visit["rejection_reason"] is None


@nodatabase
def test_update_block_visit_status_with_rejection_reason(
    db_connection: Connection,
) -> None:
    # Set the status to "Accepted"
    block_repository = create_block_repository(db_connection)
    block_visit_id = 2300  # The status for this block visit is "In queue"
    block_repository.update_block_visit_status(block_visit_id, "Accepted", None)
    block_visit = block_repository.get_block_visit(block_visit_id)
    assert block_visit["status"] == "Accepted"
    assert block_visit["rejection_reason"] is None

    # Now set it to "Rejected"
    block_repository.update_block_visit_status(
        block_visit_id, "Rejected", "Telescope technical problems"
    )
    block_visit = block_repository.get_block_visit(block_visit_id)
    assert block_visit["status"] == "Rejected"
    assert block_visit["rejection_reason"] == "Telescope technical problems"


@nodatabase
def test_update_block_visit_status_can_be_repeated(db_connection: Connection) -> None:
    # Set the status to "Accepted"
    block_repository = create_block_repository(db_connection)
    block_visit_id = 2300  # The status for this block visit is "In queue"
    block_repository.update_block_visit_status(block_visit_id, "Accepted", None)
    block_visit = block_repository.get_block_visit(block_visit_id)
    assert block_visit["status"] == "Accepted"
    assert block_visit["rejection_reason"] is None

    # Now set it to "Accepted" again
    block_repository.update_block_visit_status(block_visit_id, "Accepted", None)
    block_visit = block_repository.get_block_visit(block_visit_id)
    assert block_visit["status"] == "Accepted"
    assert block_visit["rejection_reason"] is None


@nodatabase
def test_update_block_visit_status_raises_error_for_wrong_block_id(
    db_connection: Connection,
) -> None:
    block_repository = create_block_repository(db_connection)
    with pytest.raises(NotFoundError):
        block_repository.update_block_visit_status(0, "Accepted", None)


@nodatabase
def test_update_block_visit_status_raises_error_for_deleted_block_status(
    db_connection: Connection,
) -> None:
    block_repository = create_block_repository(db_connection)
    with pytest.raises(NotFoundError):
        block_repository.update_block_visit_status(1234567890, "Deleted", None)


@nodatabase
def test_update_block_visit_status_raises_error_for_wrong_status(
    db_connection: Connection,
) -> None:
    block_repository = create_block_repository(db_connection)
    with pytest.raises(ValueError) as excinfo:
        block_repository.update_block_visit_status(1, "Wrong block visit status", None)
    assert "block visit status" in str(excinfo.value)
