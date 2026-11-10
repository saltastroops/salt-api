import asyncio
from datetime import date, datetime
from unittest.mock import MagicMock

import httpx
from fastapi.encoders import jsonable_encoder

from saltapi.main import app
from saltapi.web.api import proposals as proposals_api
from saltapi.web.schema.proposal import ProprietaryPeriodRequest


def test_proprietary_period_request_schema() -> None:
    data = {
        "id": 1,
        "proposal_code": "2020-2-MLT-007",
        "grant_reason": None,
        "granted_period": None,
        "release_date": date(2027, 4, 1),
        "current_request": {
            "request_motivation": "We have already published...",
            "made_at": datetime(2026, 4, 1, 9, 36, 7),
            "requester": "Matchett Natalie",
            "requester_email": "natmatch98@gmail.com",
            "requested_period": 36,
        },
        "previous_requests": [],
    }

    proposal_req = ProprietaryPeriodRequest(**data)
    assert proposal_req.proposal_code == "2020-2-MLT-007"
    assert proposal_req.grant_reason is None
    assert proposal_req.granted_period is None
    assert proposal_req.current_request.request_motivation == "We have already published..."
    assert proposal_req.current_request.made_at == datetime(2026, 4, 1, 9, 36, 7)
    assert proposal_req.current_request.requester == "Matchett Natalie"
    assert proposal_req.current_request.requester_email == "natmatch98@gmail.com"
    assert proposal_req.current_request.requested_period == 36


def test_proprietary_period_request_serializes_history() -> None:
    data = {
        "id": 1,
        "proposal_code": "2020-2-MLT-007",
        "grant_reason": "Approved by Chair",
        "granted_period": 36,
        "release_date": "2027-04-01",
        "current_request": {
            "request_motivation": "Latest request",
            "made_at": datetime(2026, 4, 1, 9, 36, 7),
            "requester_email": "natmatch98@gmail.com",
            "requester": "Matchett Natalie",
            "requested_period": 36,
        },
        "previous_requests": [
            {
                "request_motivation": "Earlier request",
                "made_at": datetime(2025, 4, 1, 9, 36, 7),
                "requester_email": "natmatch98@gmail.com",
                "requester": "Matchett Natalie",
                "requested_period": 24,
            }
        ],
    }

    request = ProprietaryPeriodRequest(**data)
    response = jsonable_encoder(request)

    assert response["id"] == 1
    assert response["grant_reason"] == "Approved by Chair"
    assert response["granted_period"] == 36
    assert response["release_date"] == "2027-04-01"
    assert response["current_request"]["request_motivation"] == "Latest request"
    assert (
        response["previous_requests"][0]["request_motivation"] == "Earlier request"
    )
    assert response["previous_requests"][0]["made_at"] == "2025-04-01T09:36:07"
    assert "request_reason" not in response["current_request"]


def test_requesting_more_time_endpoint_serializes_proprietary_period_request(
    monkeypatch,
) -> None:
    request_data = {
        "id": 3,
        "proposal_code": "2020-2-MLT-007",
        "grant_reason": None,
        "granted_period": None,
        "release_date": date(2027, 4, 1),
        "current_request": {
            "requester": "Matchett Natalie",
            "requester_email": "natmatch98@gmail.com",
            "made_at": datetime(2026, 4, 1, 9, 36, 7),
            "requested_period": 36,
            "request_motivation": "Latest request",
        },
        "previous_requests": [
            {
                "requester": "Matchett Natalie",
                "requester_email": "natmatch98@gmail.com",
                "made_at": datetime(2025, 4, 1, 9, 36, 7),
                "requested_period": 24,
                "request_motivation": "Earlier request",
            }
        ],
    }
    unit_of_work = MagicMock()
    unit_of_work.__enter__.return_value = unit_of_work
    permission_service = MagicMock()
    proposal_service = MagicMock()
    proposal_service.proposals_requesting_proprietary_request_extension.return_value = [
        request_data
    ]
    monkeypatch.setattr(proposals_api, "UnitOfWork", lambda: unit_of_work)
    monkeypatch.setattr(
        proposals_api.services,
        "permission_service",
        lambda connection: permission_service,
    )
    monkeypatch.setattr(
        proposals_api.services,
        "proposal_service",
        lambda connection: proposal_service,
    )
    monkeypatch.setitem(
        app.dependency_overrides,
        proposals_api.get_current_user,
        lambda: MagicMock(),
    )

    async def get_response() -> httpx.Response:
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app), base_url="http://test"
        ) as client:
            return await client.get("/proposals/proprietory-period-extention-requets")

    response = asyncio.run(get_response())

    assert response.status_code == 200
    serialized_request = response.json()[0]
    assert serialized_request["id"] == 3
    assert serialized_request["current_request"]["request_motivation"] == "Latest request"
    assert serialized_request["previous_requests"][0]["request_motivation"] == (
        "Earlier request"
    )
    assert "request_reason" not in serialized_request