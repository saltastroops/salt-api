from typing import Any, Callable

import pytest
from fastapi.testclient import TestClient
from starlette import status

from saltapi.settings import get_settings
from tests.conftest import authenticate, not_authenticated

PROGRESS_REPORT_URL = "/progress"

USERNAME = "cmofokeng"

PROPOSALS_DIR = get_settings().proposals_dir


def test_get_progress_report_returns_401_for_non_authenticated_user(
    client: TestClient,
) -> None:
    semester = "2018-2"
    proposal_code = "2018-2-LSP-001"
    not_authenticated(client)
    response = client.get(PROGRESS_REPORT_URL + "/" + proposal_code + "/" + semester)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_progress_report_returns_403_for_non_authorised_user(
    client: TestClient,
) -> None:
    semester = "2018-2"
    proposal_code = "2018-2-LSP-001"
    authenticate("TestUser", client)
    response = client.get(PROGRESS_REPORT_URL + "/" + proposal_code + "/" + semester)

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_get_progress_report_returns_404_for_wrong_proposal_code(
    client: TestClient,
) -> None:
    semester = "2022-1"
    proposal_code = "2099-1-SCI-001"
    authenticate(USERNAME, client)
    response = client.get(PROGRESS_REPORT_URL + "/" + proposal_code + "/" + semester)

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.parametrize(
    "proposal_code,semester",
    [
        ("2022-1-COM-002", "2022-2"),
        ("2018-2-GWE-002", "2018-2"),
        ("2017-2-COM-001", "2017-2"),
        ("2019-2-DDT-006", "2019-2"),
    ],
)
def test_get_progress_report_returns_empty_report_for_nonexisting_progress_report(
    proposal_code: str,
    semester: str,
    client: TestClient,
    check_data: Callable[[Any], None],
) -> None:
    authenticate(USERNAME, client)

    response = client.get(PROGRESS_REPORT_URL + "/" + proposal_code + "/" + semester)

    proposal_progress_report = response.json()

    check_data(proposal_progress_report)


def test_get_returns_progress_report_for_authorised_user(
    client: TestClient, check_data: Callable[[Any], None]
) -> None:
    semester = "2020-2"
    proposal_code = "2020-2-SCI-035"
    authenticate(USERNAME, client)

    response = client.get(PROGRESS_REPORT_URL + "/" + proposal_code + "/" + semester)

    proposal_progress_report = response.json()

    check_data(proposal_progress_report)


# TODO: Properly handle getting pdf files
@pytest.mark.skip(
    reason="This will be tested once the pdf files are handled correctly."
)
def test_get_returns_correct_pdf_files(
    client: TestClient,
) -> None:
    semester = "2018-2"
    proposal_code = "2018-2-LSP-001"

    authenticate(USERNAME, client)

    response = client.get(PROGRESS_REPORT_URL + "/" + proposal_code + "/" + semester)

    proposal_progress_report = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert proposal_progress_report["semester"] == semester
    assert proposal_progress_report["proposal_progress_pdf"] is not None

    assert (
        proposal_code + "/" + semester + "/" + "report.pdf"
    ) in proposal_progress_report["proposal_progress_pdf"]
    assert (
        proposal_code + "/" + semester + "/" + "supplementary-file.pdf"
    ) in proposal_progress_report["additional_pdf"]

    progress_pdf_response = client.get(
        proposal_progress_report["proposal_progress_pdf"]
    )

    assert progress_pdf_response.headers[
        "content-disposition"
    ] == 'attachment; filename="{}"'.format("ProgressReport_{}.pdf".format(semester))
    assert progress_pdf_response.headers["content-type"] == "application/pdf"

    additional_pdf_response = client.get(proposal_progress_report["additional_pdf"])

    assert additional_pdf_response.headers[
        "content-disposition"
    ] == 'attachment; filename="{}"'.format(
        "ProgressReportSupplement_{}.pdf".format(semester)
    )
    assert additional_pdf_response.headers["content-type"] == "application/pdf"


@pytest.mark.parametrize(
    "proposal_code,semester",
    [
        ("2019-2-SCI-003", "2019-2"),
        ("2017-1-SCI-031", "2017-1"),
        ("2020-2-SCI-035", "2020-2"),
    ],
)
def test_get_returns_progress_report(
    proposal_code: str,
    semester: str,
    client: TestClient,
    check_data: Callable[[Any], None],
) -> None:
    authenticate(USERNAME, client)

    response = client.get(PROGRESS_REPORT_URL + "/" + proposal_code + "/" + semester)

    assert response.status_code == status.HTTP_200_OK

    proposal_progress_report = response.json()

    check_data(proposal_progress_report)
