from typing import Any, Callable, cast

import pytest
from sqlalchemy.engine import Connection

from saltapi.repository.institution_repository import InstitutionRepository
from saltapi.service.institution import NewInstitutionDetails


@pytest.mark.parametrize(
    "institution_name",
    [
        "Adam Mickiewicz University",
        "ASTRON",
        "Caltech-IPAC",
        "University of Northwest Mafikeng",
        "University of Wisconsin-Madison",
    ],
)
def test_get_institution_by_name(
    db_connection: Connection, check_data: Callable[[Any], None], institution_name
) -> None:
    institution_repository = InstitutionRepository(db_connection)
    institution = institution_repository.get_institution_by_name(institution_name)
    check_data(institution)


def test_create_an_existing_institution(db_connection: Connection) -> None:
    institution_repository = InstitutionRepository(db_connection)
    institution = {
        "institution_name": "Adam Mickiewicz University",
        "department": "Physics",
        "address": "1 Example StreetExample0001",
        "url": "www.example.com",
    }
    new_institution_details = NewInstitutionDetails(**institution)
    with pytest.raises(ValueError) as excinfo:
        institution_repository.create(new_institution_details)
    assert "exists already" in str(excinfo)


def test_create_an_institution(db_connection: Connection) -> None:
    institution_repository = InstitutionRepository(db_connection)
    institution = {
        "institution_name": "University of Example",
        "department": "Example Department",
        "address": "1 Example StreetExample0001",
        "url": "www.example.com",
    }
    new_institution_details = NewInstitutionDetails(**institution)
    institution_repository.create(new_institution_details)
    institution = institution_repository.get_institution_by_name(
        new_institution_details.institution_name
    )

    assert new_institution_details.institution_name == institution["institution_name"]
    assert new_institution_details.department == institution["department"]
