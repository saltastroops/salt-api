"""Tests for the proposal service."""
import pytest
from aiomysql import Pool
from syrupy.assertion import SnapshotAssertion

from app.models.general import Semester
from app.models.proposal import (
    ObservedTime,
    Partner,
    PartnerPercentage,
    RequestedTime,
    TimeAllocation,
)
from app.service.proposal import (
    get_block_visits,
    get_observed_time,
    get_phase,
    get_requested_time,
    get_text_content,
    get_time_allocations,
)
from tests.markers import nodatabase


@nodatabase
@pytest.mark.asyncio
async def test_get_text_content_return_correct_result(db: Pool) -> None:
    """get_text_content return correct proposal text"""
    text_content = await get_text_content("2020-1-MLT-005", db)
    assert "and Kinematics of Multi-phase Gas" in text_content[0].title
    assert "providing an excellent tracer of dynamical mass" in text_content[0].abstract
    assert "Specific notes and instructions to observer:" in text_content[0].read_me


@nodatabase
@pytest.mark.asyncio
async def test_get_proposal_allocations_return_correct_result(db: Pool) -> None:
    """get_time_allocations return correct allocations."""
    # Expected result. All TAC comments have been removed.
    expected = [
        TimeAllocation(
            semester=Semester(semester=1, year=2020),
            partner=Partner(code="UW", name="University of Wisconsin-Madison"),
            tac_comment="",
            priority_0=0,
            priority_1=0,
            priority_2=0,
            priority_3=0,
            priority_4=0,
        ),
        TimeAllocation(
            semester=Semester(semester=1, year=2020),
            partner=Partner(code="RU", name="Rutgers University"),
            tac_comment="",
            priority_0=0,
            priority_1=0,
            priority_2=0,
            priority_3=0,
            priority_4=0,
        ),
        TimeAllocation(
            semester=Semester(semester=2, year=2020),
            partner=Partner(code="UW", name="University of Wisconsin-Madison"),
            tac_comment="",
            priority_0=0,
            priority_1=0,
            priority_2=0,
            priority_3=0,
            priority_4=0,
        ),
        TimeAllocation(
            semester=Semester(semester=2, year=2020),
            partner=Partner(code="RU", name="Rutgers University"),
            tac_comment="",
            priority_0=0,
            priority_1=0,
            priority_2=0,
            priority_3=0,
            priority_4=0,
        ),
    ]
    proposal_allocations = await get_time_allocations("2020-1-MLT-005", db)

    # Check TAC comments
    sem_2020_2 = Semester(year=2020, semester=2)
    uw_2020_2 = [
        a
        for a in proposal_allocations
        if a.semester == sem_2020_2 and a.partner.code == "UW"
    ][0]
    ru_2020_2 = [
        a
        for a in proposal_allocations
        if a.semester == sem_2020_2 and a.partner.code == "RU"
    ][0]
    assert (
        uw_2020_2.tac_comment
        and "program" in uw_2020_2.tac_comment
        and "expected" in uw_2020_2.tac_comment
    )
    assert (
        ru_2020_2.tac_comment
        and "time" in ru_2020_2.tac_comment
        and "request" in ru_2020_2.tac_comment
    )

    # Remove all comments, as they are not included in the object to compare against
    for a in proposal_allocations:
        a.tac_comment = ""

    assert proposal_allocations == expected


@nodatabase
@pytest.mark.asyncio
async def test_get_proposal_requested_time_return_correct_result(
    db: Pool,
) -> None:
    """get_requested_time return correct requested time."""
    # Expected result. All comments have been removed.
    expected = [
        RequestedTime(
            total_requested_time=127000,
            minimum_useful_time=20000,
            comment=None,
            semester=Semester(semester=1, year=2021),
            distribution=[
                PartnerPercentage(
                    partner=Partner(code="RSA", name="South Africa"), percentage=80
                ),
                PartnerPercentage(
                    partner=Partner(code="UKSC", name="UK SALT Consortium"),
                    percentage=20,
                ),
            ],
        ),
        RequestedTime(
            total_requested_time=76000,
            minimum_useful_time=20000,
            comment=None,
            semester=Semester(semester=2, year=2021),
            distribution=[
                PartnerPercentage(
                    partner=Partner(code="RSA", name="South Africa"), percentage=80
                ),
                PartnerPercentage(
                    partner=Partner(code="UKSC", name="UK SALT Consortium"),
                    percentage=20,
                ),
            ],
        ),
        RequestedTime(
            total_requested_time=127000,
            minimum_useful_time=20000,
            comment=None,
            semester=Semester(semester=1, year=2022),
            distribution=[
                PartnerPercentage(
                    partner=Partner(code="RSA", name="South Africa"), percentage=80
                ),
                PartnerPercentage(
                    partner=Partner(code="UKSC", name="UK SALT Consortium"),
                    percentage=20,
                ),
            ],
        ),
        RequestedTime(
            total_requested_time=76000,
            minimum_useful_time=20000,
            comment=None,
            semester=Semester(semester=2, year=2022),
            distribution=[
                PartnerPercentage(
                    partner=Partner(code="RSA", name="South Africa"), percentage=80
                ),
                PartnerPercentage(
                    partner=Partner(code="UKSC", name="UK SALT Consortium"),
                    percentage=20,
                ),
            ],
        ),
    ]

    # Check the comments
    proposal_requested_time = await get_requested_time("2021-1-MLT-005", db)
    for prt in proposal_requested_time:
        if prt.semester.year == 2021 and prt.semester.semester == 1:
            assert (
                prt.comment
                and "based on" in prt.comment
                and "spectroscopy" in prt.comment
            )
        else:
            assert prt.comment is None

    # Remove all the comments, as they are not included in the object to compare against
    for prt in proposal_requested_time:
        prt.comment = None

    assert proposal_requested_time == expected


@nodatabase
@pytest.mark.asyncio
async def test_get_observed_time_return_correct_result(db: Pool) -> None:
    """get_observed_time return correct charged time."""
    expected = [
        ObservedTime(
            semester=Semester(year=2017, semester=1),
            priority_0=0,
            priority_1=0,
            priority_2=4614,
            priority_3=2307,
            priority_4=0,
        )
    ]
    observed_time = await get_observed_time("2017-1-SCI-003", db)
    assert observed_time == expected


@nodatabase
@pytest.mark.asyncio
@pytest.mark.parametrize("proposal_code", ("2017-1-SCI-005", "2020-1-SCI-020"))
async def test_get_block_visits_return_correct_result(
    proposal_code: str, db: Pool, snapshot: SnapshotAssertion
) -> None:
    """get_block_visits return correct targets."""

    block_visits = await get_block_visits(proposal_code, db)
    sorted_block_visits = sorted(block_visits, key=lambda i: i.block_visit_id)

    assert sorted_block_visits == snapshot


@nodatabase
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "proposal_code,phase", (("2020-2-SCI-043", 2), ("2019-2-SCI-009", 1))
)
async def test_get_phase_returns_correct_result(
    proposal_code: str, phase: int, db: Pool
) -> None:
    assert await get_phase(proposal_code, db) == phase
