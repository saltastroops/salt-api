from typing import Dict, Any

import pytest
from fastapi.testclient import TestClient
from starlette import status

from tests.conftest import not_authenticated, misauthenticate, authenticate, find_username

TEST_DATA = "integration/users/get_user.yaml"

PROPOSALS_URL = "{proposal_code}/proprietary_period"


def _url(proposal_code: str) -> str:
    return "/proposals/" + proposal_code + "/proprietary_period/"


def test_update_proprietary_period_should_return_401_for_unauthenticated_user(client: TestClient) -> None:
    not_authenticated(client)
    proposal_code = "2020-1-SCI-005"
    response = client.put(_url(proposal_code), )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_update_proprietary_period_should_return_401_for_user_with_invalid_auth_token(
        client: TestClient
) -> None:
    misauthenticate(client)
    proposal_code = "2020-1-SCI-005"
    response = client.put(_url(proposal_code), )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.parametrize(
    "proposal_code,proprietary_period_update",
    [
       ("2020-1-SCI-005", {"proprietary_period": 0, "motivation": None}),  # RSA allocated time
       ("2020-1-SCI-005", {"proprietary_period": 10, "motivation": None}),  # RSA allocated time
       ("2020-1-SCI-005", {"proprietary_period": 24, "motivation": None}),  # RSA allocated time
       ("2020-1-SCI-005", {"proprietary_period": 25, "motivation": None}),  # RSA allocated time
       ("2020-1-SCI-005", {"proprietary_period": 10000, "motivation": None}),  # RSA allocated time
       ("2020-1-MLT-005", {"proprietary_period": 0, "motivation": None}),  # RSA allocated no time
       ("2020-1-MLT-005", {"proprietary_period": 10, "motivation": None}),  # RSA allocated no time
       ("2020-1-MLT-005", {"proprietary_period": 10000, "motivation": None}),  # RSA allocated no time
       ("2016-1-COM-001", {"proprietary_period": 10000, "motivation": None}),
       ("2016-1-SVP-001", {"proprietary_period": 10000, "motivation": None}),
       ("2019-1-GWE-005", {"proprietary_period": 10000, "motivation": None}),
       ("2022-1-ORP-001", {"proprietary_period": 10000, "motivation": None}),
       ("2020-2-DDT-005", {"proprietary_period": 10000, "motivation": None}),

    ],
)
def test_update_proprietary_period_should_allow_admins_to_make_any_requests(
        proposal_code: str, proprietary_period_update: Dict[str, Any], client: TestClient
) -> None:
    admin = find_username("Administrator")
    authenticate(admin, client)
    response = client.put(_url(proposal_code), json=proprietary_period_update)
    assert response.status_code == status.HTTP_202_ACCEPTED
    assert response.json()["status"] == "Successful"


@pytest.mark.parametrize(
    "proposal_code,proprietary_period_update",
    [
        ("2019-2-SCI-006", {"proprietary_period": 10, "motivation": None}),  # RSA allocated time
        ("2020-1-MLT-005", {"proprietary_period": 10, "motivation": None}),  # RSA allocated no time
        ("2016-1-COM-001", {"proprietary_period": 5, "motivation": None}),
        ("2016-1-SVP-001", {"proprietary_period": 5, "motivation": None}),
        ("2019-1-GWE-005", {"proprietary_period": 5, "motivation": None}),
        ("2022-1-ORP-001", {"proprietary_period": 5, "motivation": None}),
        ("2020-2-DDT-005", {"proprietary_period": 5, "motivation": None}),

    ],
)
def test_update_proprietary_period_should_allow_pis_to_update_without_motivations(
        proposal_code: str, proprietary_period_update: Dict[str, Any], client: TestClient
) -> None:
    pi = find_username("Principal Investigator", proposal_code)
    authenticate(pi, client)
    response = client.put(_url(proposal_code), json=proprietary_period_update)
    assert response.status_code == status.HTTP_202_ACCEPTED
    assert response.json()["status"] == "Successful"


def test_update_proprietary_period_should_not_allow_admins_to_make_illegal_requests(
        client: TestClient
) -> None:
    #  Administrators that are an investigator to a proposal are not allowed to update proprietary period
    #  with more time than what the partner requires.
    admin_investigator = find_username("Administrator Investigator")
    authenticate(admin_investigator, client)
    proposal_code = "2022-1-MLT-003"  # RSA allocated time
    proprietary_period_update = {
        "proprietary_period": 25,   # RSA proposals have maximum of 24 months
        "motivation": None          # They require motivation for proprietary period higher than 24 month
    }
    with pytest.raises(ValueError) as excinfo:
        client.put(_url(proposal_code), json=proprietary_period_update)
    assert "motivation is required" in str(excinfo)


@pytest.mark.parametrize(
    "proposal_code,proprietary_period_update",
    [
        ("2018-1-SCI-037", {"proprietary_period": 25, "motivation": "This is a motivation"}),  # RSA allocated time
        ("2020-1-MLT-005", {"proprietary_period": 1201, "motivation": "This is a motivation"}),  # RSA allocated no time
        ("2016-1-COM-001", {"proprietary_period": 37, "motivation": "This is a motivation"}),
        ("2016-1-SVP-001", {"proprietary_period": 13, "motivation": "This is a motivation"}),
        ("2019-1-GWE-005", {"proprietary_period": 1201, "motivation": "This is a motivation"}),
        ("2022-1-ORP-001", {"proprietary_period": 25, "motivation": "This is a motivation"}),
        ("2020-2-DDT-005", {"proprietary_period": 30, "motivation": "This is a motivation"}),
    ],
)
def test_update_proprietary_period_should_allow_pi_to_submit_extensions_with_motivation(
        proposal_code: str, proprietary_period_update: Dict[str, Any], client: TestClient
) -> None:
    pi = find_username("Principal Investigator", proposal_code=proposal_code)
    authenticate(pi, client)
    response = client.put(_url(proposal_code), json=proprietary_period_update)
    assert response.status_code == status.HTTP_202_ACCEPTED
    assert response.json()["status"] == "Pending"

@pytest.mark.parametrize(
    "proposal_code,proprietary_period_update",
    [
        ("2019-2-SCI-006", {"proprietary_period": 25, "motivation": "This is a motivation"}),  # RSA allocated time
        ("2016-1-SCI-018", {"proprietary_period": 25, "motivation": "This is a motivation"}),
        ("2016-1-SVP-001", {"proprietary_period": 13, "motivation": "This is a motivation"}),
        ("2020-2-DDT-005", {"proprietary_period": 30, "motivation": "This is a motivation"}),
    ],
)
def test_update_proprietary_period_should_not_allow_investigators_to_submit_extensions(
        proposal_code: str, proprietary_period_update: Dict[str, Any], client: TestClient
) -> None:
    pi = find_username("Investigator", proposal_code=proposal_code)
    authenticate(pi, client)
    response = client.put(_url(proposal_code), json=proprietary_period_update)
    assert response.status_code == status.HTTP_403_FORBIDDEN

