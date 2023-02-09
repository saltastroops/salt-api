import pathlib
from typing import Any, NamedTuple

import pytest
from fastapi.testclient import TestClient
from starlette import status

from tests.conftest import authenticate, find_username

PROGRESS_REPORT_URL = "/progress"


def test_submit_progress_report(
    client: TestClient, tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    class MockSettings(NamedTuple):
        proposals_dir: pathlib.Path

    def mock_get_settings() -> Any:
        return MockSettings(pathlib.Path(tmp_path))

    monkeypatch.setattr(
        "saltapi.service.proposal_service.get_settings", mock_get_settings
    )

    proposal_code = "2020-2-SCI-043"
    proposal_dir = mock_get_settings().proposals_dir / proposal_code
    included_dir = proposal_dir / "Included"
    # The included directory must exist as the generated progress report is stored in
    # that directory.
    included_dir.mkdir(parents=True)
    submission_version_dir = proposal_dir / "1"
    submission_version_dir.mkdir(parents=True)

    summary_pdf: pathlib.Path = submission_version_dir / "Summary.pdf"
    fake_summary_pdf = pathlib.Path.cwd() / "tests" / "data" / "summary.pdf"
    summary_pdf.write_bytes(fake_summary_pdf.read_bytes())

    data = {
        "requested_time": 4200,
        "maximum_seeing": 2,
        "transparency": "Thin cloud",
        "description_of_observing_constraints": 'Thin/thick cloud and 2-3" seeing.',
        "change_reason": "N/A",
        "summary_of_proposal_status": "See attached.",
        "strategy_changes": "None",
        "partner_requested_percentages": "RSA:100;OTH:0",
    }
    username = find_username("administrator")
    authenticate(username, client)

    response = client.put(
        PROGRESS_REPORT_URL + "/" + proposal_code + "/2020-2", data=data
    )
    assert response.status_code == status.HTTP_200_OK
