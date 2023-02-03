from typing import Dict, List, Optional, cast

import pytest

from saltapi.exceptions import AuthorizationError, NotFoundError
from saltapi.repository.proposal_repository import ProposalRepository
from saltapi.service.proposal import ProposalListItem
from saltapi.service.proposal_service import ProposalService
from saltapi.web.schema.proposal import ProposalStatus, ProposalStatusValue


class FakeProposalRepository:
    def __init__(self) -> None:
        self.proposal_status = {"value": "Under scientific review", "reason": None}

    def list(
        self, username: str, from_semester: str, to_semester: str, limit: str
    ) -> List[ProposalListItem]:
        return [
            cast(ProposalListItem, from_semester),
            cast(ProposalListItem, to_semester),
            cast(ProposalListItem, limit),
        ]

    def get_proposal_status(self, proposal_code: str) -> Dict[str, str]:
        if proposal_code == VALID_PROPOSAL_CODE:
            return self.proposal_status
        raise NotFoundError()

    def update_proposal_status(
        self,
        proposal_code: str,
        proposal_status_value: str,
        inactive_reason: Optional[str],
    ) -> None:
        if proposal_code == VALID_PROPOSAL_CODE:
            if proposal_status_value not in ProposalStatusValue.value:
                raise AuthorizationError()
            self.proposal_status = {
                "value": proposal_status_value,
                "reason": inactive_reason,
            }
        else:
            raise NotFoundError()


def create_proposal_repository() -> ProposalService:
    proposal_repository = FakeProposalRepository()
    proposal_service = ProposalService(cast(ProposalRepository, proposal_repository))
    return proposal_service


VALID_PROPOSAL_CODE = "2023-1-MLT-006"


def test_list_proposal_summaries_returns_correct_proposals() -> None:
    proposal_service = create_proposal_repository()
    assert proposal_service.list_proposal_summaries(
        username="someone", from_semester="2019-1", to_semester="2020-1"
    ) == ["2019-1", "2020-1", 1000]
    assert proposal_service.list_proposal_summaries(
        username="someone", from_semester="2019-1"
    ) == ["2019-1", "2099-2", 1000]
    assert proposal_service.list_proposal_summaries(
        username="someone", to_semester="2020-1"
    ) == ["2000-1", "2020-1", 1000]
    assert proposal_service.list_proposal_summaries(username="someone", limit=67) == [
        "2000-1",
        "2099-2",
        67,
    ]


def test_list_proposal_summaries_raises_error_for_negative_limit() -> None:
    proposal_service = create_proposal_repository()
    with pytest.raises(ValueError) as excinfo:
        proposal_service.list_proposal_summaries(
            username="someone", from_semester="2019-1", to_semester="2019-2", limit=-1
        )
    assert "negative" in str(excinfo.value)


def test_list_proposal_summaries_raises_error_from_wrong_semester_order() -> None:
    proposal_service = create_proposal_repository()
    with pytest.raises(ValueError) as excinfo:
        proposal_service.list_proposal_summaries(
            username="someone", from_semester="2019-1", to_semester="2018-2"
        )
    assert "semester" in str(excinfo.value)


def test_get_proposal_status_raises_for_wrong_proposal_code() -> None:
    proposal_service = create_proposal_repository()
    with pytest.raises(NotFoundError):
        proposal_service.get_proposal_status("2021-2-LSP-001")


def test_get_proposal_status() -> None:
    proposal_service = create_proposal_repository()
    proposal_status = proposal_service.get_proposal_status(VALID_PROPOSAL_CODE)

    assert proposal_status["value"] == "Under scientific review"
    assert proposal_status["reason"] is None
