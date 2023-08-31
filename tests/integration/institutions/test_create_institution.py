from faker import Faker
from fastapi.testclient import TestClient
from starlette import status

INSTITUTION_URL = "/institutions"


def test_create_institution(client: TestClient) -> None:
    fake = Faker()
    institution = {
        "institution_name": f"{fake.name()} University",
        "department": "Physics",
        "address": fake.address(),
        "url": "www.world-university.com",
    }
    response = client.post(INSTITUTION_URL + "/", json=institution)
    new_institution = response.json()

    assert response.status_code == status.HTTP_201_CREATED
    assert new_institution["institution_name"] == institution["institution_name"]
    assert new_institution["department"] == institution["department"]


def test_create_an_existing_institution(client: TestClient) -> None:
    institution = {
        "institution_name": "University of the Free State",
        "department": "Physics department",
        "address": (
            "205 Nelson Mandela Dr"
            "\nUniversity of the Free State"
            "\nPhysics department"
            "\nP.O. Box 339"
            "\nBloemfontein"
            "\n9300"
            "\nSouth Africa"
        ),
        "url": "www.world-university.com",
    }
    response = client.post(INSTITUTION_URL + "/", json=institution)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
