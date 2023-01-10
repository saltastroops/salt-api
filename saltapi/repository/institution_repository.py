from typing import Any, Dict, List, cast

from sqlalchemy import text
from sqlalchemy.engine import Connection
from sqlalchemy.exc import NoResultFound

from saltapi.exceptions import NotFoundError
from saltapi.service.institution import NewInstitutionDetails


class InstitutionRepository:
    def __init__(self, connection: Connection) -> None:
        self.connection = connection

    def get_institutions(self) -> List[Dict[str, Any]]:
        """
        Returns a list of institutions
        """
        stmt = text(
            """
SELECT
    P.Partner_Code   AS partner_code,
    P.Partner_Name   AS partner_name,
    I2.Department    AS department,
    I2.Institute_Id  AS institution_id,
    I.InstituteName_Name AS name
FROM Partner P
    JOIN Institute I2 ON P.Partner_Id = I2.Partner_Id
    JOIN InstituteName I ON I2.InstituteName_Id = I.InstituteName_Id
            """
        )
        result = self.connection.execute(stmt)
        institutions = [
            {
                "institution_id": row.institution_id,
                "name": row.name,
                "department": row.department,
                "partner_code": row.partner_code,
                "partner_name": row.partner_name,
            }
            for row in result
        ]
        return institutions

    def get_institution_by_name(self, institution_name: str) -> Dict[str, Any]:
        """
        Returns the user with a given username.

        If the username does not exist, a NotFoundError is raised.
        """
        stmt = text(
            """
SELECT
    P.Partner_Code   AS partner_code,
    P.Partner_Name   AS partner_name,
    I2.Department    AS department,
    I2.Institute_Id  AS institution_id,
    I.InstituteName_Name AS name
FROM Partner P
    JOIN Institute I2 ON P.Partner_Id = I2.Partner_Id
    JOIN InstituteName I ON I2.InstituteName_Id = I.InstituteName_Id
WHERE I.InstituteName_Name = :institution_name
            """
        )
        result = self.connection.execute(
            stmt, {"institution_name": institution_name}
        )

        row = result.one()

        institution = {
            "institution_id": row.institution_id,
            "institution_name": row.name,
            "department": row.department,
            "partner_code": row.partner_code,
            "partner_name": row.partner_name,
        }

        return institution

    def _does_institution_exist(self, institution_name: str) -> bool:
        """Check whether an institution exists already."""

        try:
            self.get_institution_by_name(institution_name)
        except NotFoundError:
            return False
        except NoResultFound:
            return False

        return True

    def create(self, new_institution_details: NewInstitutionDetails) -> None:
        """Creates a new institution."""

        # Make sure the institution is still available
        if self._does_institution_exist(new_institution_details.institution_name):
            raise ValueError(
                f"The institution {new_institution_details.institution_name} exists already."
            )

        institution_name_id = self._add_institution_name(new_institution_details)
        self._create_institution_details(new_institution_details, institution_name_id)

    def _add_institution_name(self, new_institution_details: NewInstitutionDetails):
        """
        Add institution name.

        The primary key of the new database entry is returned.
        """

        stmt = text(
            """
INSERT INTO InstituteName (InstituteName_Name)
VALUES (:institution_name)
        """
        )
        result = self.connection.execute(
            stmt,
            {
                "institution_name": new_institution_details.institution_name
            },
        )

        return cast(int, result.lastrowid)

    def _create_institution_details(self, new_institution_details: NewInstitutionDetails, institution_name_id: int) -> None:
        # OTHER partner is used to create a new institution details
        partner_id = 4
        stmt = text(
            """
INSERT INTO Institute (Partner_Id, InstituteName_Id, Department, Url, Address)
VALUES (:partner_id, :institution_name_id, :department, :url, :address)
        """
        )
        self.connection.execute(
            stmt,
            {
                "partner_id": partner_id,
                "institution_name_id": institution_name_id,
                "department": new_institution_details.department,
                "url": new_institution_details.url,
                "address": new_institution_details.address,
                "institution_name": new_institution_details.institution_name
            },
        )
