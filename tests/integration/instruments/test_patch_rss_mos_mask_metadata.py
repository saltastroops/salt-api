from datetime import date

import pytest
from fastapi.testclient import TestClient
from starlette import status

from tests.conftest import authenticate, find_username, not_authenticated

RSS_MOS_MASK_METADATA_URL = "/rss/mos-mask-metadata"


def test_mos_mask_update_requires_authentication(
    client: TestClient,
) -> None:
    barcode = "P000127N03"

    not_authenticated(client)
    response = client.patch(
        RSS_MOS_MASK_METADATA_URL + "/" + barcode,
        json={"cut_by": "Chaka", "cut_date": None, "mask_comment": None},
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_mos_mask_update_requires_valid_barcode(
    client: TestClient,
) -> None:
    barcode = "P000000N00"

    user = find_username("Administrator")
    authenticate(user, client)
    response = client.patch(
        RSS_MOS_MASK_METADATA_URL + "/" + barcode,
        json={"cut_by": "Chaka", "cut_date": None, "mask_comment": None},
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.parametrize(
    "username",
    [
        find_username("Investigator", proposal_code="2019-2-SCI-006"),
        find_username("Principal Contact", proposal_code="2019-2-SCI-006"),
        find_username("Principal Investigator", proposal_code="2019-2-SCI-006"),
        find_username("TAC Member", partner_code="RSA"),
        find_username("TAC Chair", partner_code="RSA"),
    ],
)
def test_mos_mask_update_requires_requires_permissions(
    username: str, client: TestClient
) -> None:
    barcode = "P000127N03"

    authenticate(username, client)
    response = client.patch(
        RSS_MOS_MASK_METADATA_URL + "/" + barcode,
        json={"cut_by": "Chaka", "cut_date": None, "mask_comment": None},
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_mos_mask_update_cut_by(
    client: TestClient,
) -> None:
    barcode = "P000127N01"
    cut_by = "Chaka"

    user = find_username("SALT Astronomer")
    authenticate(user, client)
    response = client.patch(
        RSS_MOS_MASK_METADATA_URL + "/" + barcode,
        json={"cut_by": cut_by, "cut_date": None, "mask_comment": None},
    )
    assert response.status_code == status.HTTP_200_OK

    metadata = response.json()
    assert metadata["barcode"] == barcode
    assert metadata["cut_by"] == cut_by
    assert metadata["cut_date"] is None
    assert metadata["mask_comment"] is None


def test_mos_mask_update_cut_date_and_mask_comment(
    client: TestClient,
) -> None:
    barcode = "P000127N01"
    cut_by = "Chaka"
    cut_date = date(2021, 1, 1).isoformat()
    mask_comment = "Mask re-cut, first one bad."

    user = find_username("SALT Astronomer")
    authenticate(user, client)
    response = client.patch(
        RSS_MOS_MASK_METADATA_URL + "/" + barcode,
        json={"cut_by": cut_by, "cut_date": cut_date, "mask_comment": mask_comment},
    )
    assert response.status_code == status.HTTP_200_OK

    metadata = response.json()
    assert metadata["barcode"] == barcode
    assert metadata["cut_by"] == cut_by
    assert metadata["cut_date"] == cut_date
    assert metadata["mask_comment"] == mask_comment
