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
    check_data(response.json())
