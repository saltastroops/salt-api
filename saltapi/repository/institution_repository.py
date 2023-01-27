from typing import Any, Dict, List, cast

from sqlalchemy import text
from sqlalchemy.engine import Connection
from sqlalchemy.exc import IntegrityError, NoResultFound

from saltapi.exceptions import NotFoundError, ResourceExistsError


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

    def get_institution_by_name_and_department(
        self, institution_name: str, department: str
    ) -> Dict[str, Any]:
        """
        Return the institution with a given name and department.

        If the combination of name and department does not exist,
        a NotFoundError is raised.
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
AND I2.Department = :department
            """
        )
        result = self.connection.execute(
            stmt, {"institution_name": institution_name, "department": department}
        )

        try:
            row = result.one()

            institution = {
                "institution_id": row.institution_id,
                "institution_name": row.name,
                "department": row.department,
                "partner_code": row.partner_code,
                "partner_name": row.partner_name,
            }

            return institution
        except NoResultFound:
            raise NotFoundError("Unknown institution.")

    def _does_institution_exist(self, institution_name: str, department: str) -> bool:
        """Check whether an institution exists already."""

        try:
            self.get_institution_by_name_and_department(institution_name, department)
        except NotFoundError:
            return False

        return True

    def create(self, new_institution_details: Dict[str, Any]) -> None:
        """Creates a new institution."""

        # Make sure the institution does not exist yet
        if self._does_institution_exist(
            new_institution_details["institution_name"],
            new_institution_details["department"],
        ):
            raise ResourceExistsError(
                f"The institution {new_institution_details['institution_name']} "
                f"({new_institution_details['department']}) exists already."
            )

        institution_name_id = self._add_institution_name(new_institution_details)
        self._create_institution_details(new_institution_details, institution_name_id)

    def _add_institution_name(self, new_institution_details: Dict[str, Any]) -> int:
        """
        Add the institution name to the database.

        The primary key of the new database entry is returned.

        If the name exists already, the primary key of the existing name entry is
        returned.
        """
        try:
            stmt = text(
                """
    INSERT INTO InstituteName (InstituteName_Name)
    VALUES (:institution_name)
            """
            )
            result = self.connection.execute(
                stmt,
                {"institution_name": new_institution_details["institution_name"]},
            )

            return cast(int, result.lastrowid)
        except IntegrityError:
            stmt = text(
                """
    SELECT I.InstituteName_Id
    FROM InstituteName I
    WHERE I.InstituteName_Name = :institution_name
            """
            )
            result = self.connection.execute(
                stmt,
                {"institution_name": new_institution_details["institution_name"]},
            )

            return cast(int, result.one())

    def _create_institution_details(
        self, new_institution_details: Dict[str, Any], institution_name_id: int
    ) -> None:
        stmt = text(
            """
INSERT INTO Institute (Partner_Id, InstituteName_Id, Department, Url, Address)
VALUES ((SELECT P.Partner_Id FROM Partner P WHERE P.Partner_Name = 'Other'),
        :institution_name_id, :department, :url, :address)
FROM Partner P
WHERE P.Partner_Name = 'Other'
        """
        )
        self.connection.execute(
            stmt,
            {
                "institution_name_id": institution_name_id,
                "department": new_institution_details["department"],
                "url": new_institution_details["url"],
                "address": new_institution_details["address"],
                "institution_name": new_institution_details["institution_name"],
            },
        )
