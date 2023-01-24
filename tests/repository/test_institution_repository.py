from typing import Any, Callable

import pytest
from sqlalchemy.engine import Connection

from saltapi.exceptions import ResourceExistsError
from saltapi.repository.institution_repository import InstitutionRepository


def test_get_institution_by_name_and_department(
    db_connection: Connection, check_data: Callable[[Any], None]
) -> None:
    institution_name = "Adam Mickiewicz University"
    department = "Astronomical Observatory"
    institution_repository = InstitutionRepository(db_connection)
    institution = institution_repository.get_institution_by_name_and_department(
        institution_name, department
    )
    check_data(institution)


def test_create_an_existing_institution(db_connection: Connection) -> None:
    institution_repository = InstitutionRepository(db_connection)
    new_institution_details = {
        "institution_name": "SKA South Africa",
        "department": "",
        "address": "3rd Floor,\nThe Park,\nPark Road,\nPinelands,\n7405nSouth Africa",
        "url": "www.ska.ac.za",
    }
    with pytest.raises(ResourceExistsError) as excinfo:
        institution_repository.create(new_institution_details)
    assert "exists already" in str(excinfo)


def test_create_an_institution(db_connection: Connection) -> None:
    institution_repository = InstitutionRepository(db_connection)
    new_institution_details = {
        "institution_name": "University of Example",
        "department": "Example Department",
        "address": "1 Example Street,\nExample,\n0001",
        "url": "www.example.com",
    }
    institution_repository.create(new_institution_details)
    institution = institution_repository.get_institution_by_name_and_department(
        new_institution_details["institution_name"], new_institution_details["department"]
    )

    assert new_institution_details["institution_name"] == institution["institution_name"]
    assert new_institution_details["department"]== institution["department"]
