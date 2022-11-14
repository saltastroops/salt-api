import pytest
from fastapi.testclient import TestClient
from starlette import status

from tests.conftest import authenticate, find_username

RSS_MASKS_IN_MAGAZINE_URL = "/rss/masks-in-magazine"


def test_should_return_list_of_rss_masks_in_magazine(
    client: TestClient,
) -> None:
    response_all_masks = client.get(
        RSS_MASKS_IN_MAGAZINE_URL + "/",
    )
    assert response_all_masks.status_code == status.HTTP_200_OK

    response_longslit_masks = client.get(
        RSS_MASKS_IN_MAGAZINE_URL + "/", params={"mask_types": ["Longslit"]}
    )
    assert response_longslit_masks.status_code == status.HTTP_200_OK

    response_mos_masks = client.get(
        RSS_MASKS_IN_MAGAZINE_URL + "/",
        params={"mask_types": ["MOS"]},
    )
    assert response_mos_masks.status_code == status.HTTP_200_OK

    response_imaging_masks = client.get(
        RSS_MASKS_IN_MAGAZINE_URL + "/",
        params={"mask_types": ["Imaging"]},
    )
    assert response_imaging_masks.status_code == status.HTTP_200_OK

    response_engineering_masks = client.get(
        RSS_MASKS_IN_MAGAZINE_URL + "/",
        params={"mask_types": ["Engineering"]},
    )
    assert response_engineering_masks.status_code == status.HTTP_200_OK
    assert len(response_all_masks.json()) == sum(
        [
            len(response_longslit_masks.json()),
            len(response_mos_masks.json()),
            len(response_imaging_masks.json()),
            len(response_engineering_masks.json()),
        ]
    )


@pytest.mark.parametrize(
    "username,may_view",
    [
        (find_username("SALT Astronomer"), True),
        (find_username("Administrator"), True),
        (find_username("Board Member"), False),
        (find_username("TAC Member", partner_code="RSA"), False),
        (find_username("TAC Chair", partner_code="RSA"), False),
        (find_username("Investigator", proposal_code="2019-2-SCI-006"), False),
        (find_username("Administrator"), True),
    ],
)
def test_access_to_obsolete_masks_in_magazine_is_restricted(
    username: str, may_view: bool, client: TestClient
) -> None:
    authenticate(username, client)
    response = client.get("/rss/obsolete-masks-in-magazine")
    expected_status_code = status.HTTP_200_OK if may_view else status.HTTP_403_FORBIDDEN
    assert response.status_code == expected_status_code
