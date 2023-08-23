import enum
import hashlib
import secrets
import uuid
from typing import Any, Dict, List, cast

from passlib.context import CryptContext
from sqlalchemy import text
from sqlalchemy.engine import Connection
from sqlalchemy.exc import NoResultFound, IntegrityError

from saltapi.exceptions import NotFoundError, ResourceExistsError
from saltapi.service.user import Role, User

pwd_context = CryptContext(
    schemes=["bcrypt", "md5_crypt"], default="bcrypt", deprecated="auto"
)


class ProposalPermission(enum.Enum):
    VIEW = "View"


class UserRepository:
    def __init__(self, connection: Connection) -> None:
        self.connection = connection
        self._get_user_query = """
SELECT PU.PiptUser_Id           AS id,
       I1.Email                 AS email,
       I0.Email                 AS alternative_email,
       I0.Surname               AS family_name,
       I0.FirstName             AS given_name,
       PU.Password              AS password_hash,
       PU.Username              AS username,
       P.Partner_Code           AS partner_code,
       P.Partner_Name           AS partner_name,
       I.InstituteName_Name     AS institution_name,
       I2.Institute_Id          AS institution_id,
       I2.Department            AS department
FROM PiptUser AS PU
         JOIN Investigator AS I0 ON PU.PiptUser_Id = I0.PiptUser_Id
         JOIN Investigator I1 ON PU.Investigator_Id = I1.Investigator_Id
         JOIN Institute I2 ON I0.Institute_Id = I2.Institute_Id
         JOIN Partner P ON I2.Partner_Id = P.Partner_Id
         JOIN InstituteName I ON I2.InstituteName_Id = I.InstituteName_Id
"""

    def _get(self, rows: Any) -> User:
        user = {}
        for i, row in enumerate(rows):
            if i == 0:
                user = {
                    "id": row.id,
                    "username": row.username,
                    "family_name": row.family_name,
                    "given_name": row.given_name,
                    "email": row.email,
                    "alternative_emails": [row.alternative_email]
                    if row.alternative_email != row.email
                    else [],
                    "password_hash": row.password_hash,
                    "affiliations": [
                        {
                            "institution_id": row.institution_id,
                            "name": row.institution_name,
                            "department": row.department,
                            "partner_code": row.partner_code,
                            "partner_name": row.partner_name,
                        }
                    ],
                }
            else:
                if row.alternative_email != row.email:
                    user["alternative_emails"].append(row.alternative_email)
                user["affiliations"].append(
                    {
                        "institution_id": row.institution_id,
                        "name": row.institution_name,
                        "department": row.department,
                        "partner_code": row.partner_code,
                        "partner_name": row.partner_name,
                    }
                )
        if not user:
            raise NotFoundError("Unknown username")
        return User(**user, roles=self.get_user_roles(user["username"]))

    def get_by_username(self, username: str) -> User:
        """
        Returns the user with a given username.

        If the username does not exist, a NotFoundError is raised.
        """
        query = self._get_user_query + """WHERE PU.Username = :username"""
        stmt = text(query)
        result = self.connection.execute(stmt, {"username": username})
        user = self._get(result)
        return user

    def get(self, user_id: int) -> User:
        """
        Returns the user with a given user id.

        If there is no such user, a NotFoundError is raised.
        """
        query = self._get_user_query + """\nWHERE PU.PiptUser_Id = :user_id"""
        stmt = text(query)
        result = self.connection.execute(stmt, {"user_id": user_id})
        user = self._get(result)
        return user

    def get_by_email(self, email: str) -> User:
        """
        Returns the user with a given email

        If there is no such user, a NotFoundError is raised.
        """
        query = self._get_user_query + """\nWHERE I1.Email = :email"""
        stmt = text(query)
        result = self.connection.execute(stmt, {"email": email})
        user = self._get(result)
        return user

    def is_existing_user_id(self, user_id: int) -> bool:
        """
        Return whether a user id exists.
        """

        stmt = text(
            """
SELECT COUNT(*) AS user_count FROM PiptUser WHERE PiptUser_Id=:user_id
        """
        )
        result = self.connection.execute(stmt, {"user_id": user_id})

        return cast(int, result.scalar_one()) > 0

    def get_users(self) -> List[Dict[str, Any]]:
        """
        Returns a list of users information
        """
        stmt = text(
            """
SELECT DISTINCT PU.PiptUser_Id          AS id,
                PU.Username             AS username,
                I.FirstName             AS given_name,
                I.Surname               AS family_name
FROM PiptUser PU
         JOIN Investigator I ON I.Investigator_Id = PU.Investigator_Id
WHERE I.FirstName != 'Guest'
ORDER BY I.Surname, I.FirstName
        """
        )

        result = self.connection.execute(stmt)

        users = [
            {
                "id": row.id,
                "username": row.username,
                "given_name": row.given_name,
                "family_name": row.family_name,
            }
            for row in result
        ]
        return users

    def create(self, new_user_details: Dict[str, Any]) -> None:
        """Creates a new user."""

        # Make sure the username is still available
        if self._does_username_exist(new_user_details["username"]):
            raise ValueError(
                f"The username {new_user_details['username']} exists already."
            )

        investigator_id = self._create_investigator_details(new_user_details)
        pipt_user_id = self._create_pipt_user(new_user_details, investigator_id)
        self._add_investigator_to_pipt_user(pipt_user_id, investigator_id)
        self._update_user_statistics(
            pipt_user_id,
            dict(
                legal_status=new_user_details["legal_status"],
                gender=new_user_details["gender"],
                race=new_user_details["race"],
                has_phd=new_user_details["has_phd"],
                year_of_phd_completion=new_user_details["year_of_phd_completion"],
            ),
        )

    def _create_investigator_details(self, new_user_details: Dict[str, Any]) -> int:
        """
        Create investigator details.

        The primary key of the new database entry is returned.
        """

        stmt = text(
            """
INSERT INTO Investigator (Institute_Id, FirstName, Surname, Email)
VALUES (:institution_id, :given_name, :family_name, :email)
        """
        )
        result = self.connection.execute(
            stmt,
            {
                "institution_id": new_user_details["institution_id"],
                "given_name": new_user_details["given_name"],
                "family_name": new_user_details["family_name"],
                "email": new_user_details["email"],
            },
        )

        return cast(int, result.lastrowid)

    def _create_pipt_user(
        self, new_user_details: Dict[str, Any], investigator_id: int
    ) -> int:
        # TODO: Uncomment once the Password table exists.
        password = new_user_details["password"]
        # self._update_password_hash(username, password)
        password_hash = self.get_password_hash(password)

        stmt = text(
            """
INSERT INTO PiptUser (Username, Password, Investigator_Id, EmailValidation, Active)
VALUES (:username, :password_hash, :investigator_id, :email_validation, 0)
        """
        )
        result = self.connection.execute(
            stmt,
            {
                "username": new_user_details["username"],
                "password_hash": password_hash,
                "investigator_id": investigator_id,
                "email_validation": str(uuid.uuid4())[:8],
            },
        )

        return cast(int, result.lastrowid)

    def _add_investigator_to_pipt_user(
        self, pipt_user_id: int, investigator_id: int
    ) -> None:
        stmt = text(
            """
UPDATE Investigator
SET PiptUser_Id = :pipt_user_id
WHERE Investigator_Id = :investigator_id
        """
        )
        self.connection.execute(
            stmt, {"pipt_user_id": pipt_user_id, "investigator_id": investigator_id}
        )

    def _does_username_exist(self, username: str) -> bool:
        """Check whether a username exists already."""
        try:
            self.get_by_username(username)
        except NotFoundError:
            return False

        return True

    def update(self, user_id: int, user_update: Dict[str, Any]) -> None:
        """
        Updates a user's details.

        If the user id does not exist, a NotFoundError is raised.
        If the email exists already and belongs to another user, a ValueError is raised.

        """
        if not self.is_existing_user_id(user_id):
            raise NotFoundError(f"Unknown user id: {user_id}")

        try:
            user = self.get_by_email(user_update["email"])
            if user.id != user_id:
                raise ResourceExistsError(
                    f"The email {user_update['email']} exists already."
                )
        except NotFoundError:
            pass

        if user_update["password"]:
            self.update_password(user_id, user_update["password"])

        self._update_user_details(user_id, user_update)

        self._update_user_statistics(
            user_id,
            dict(
                legal_status=user_update["legal_status"],
                gender=user_update["gender"],
                race=user_update["race"],
                has_phd=user_update["has_phd"],
                year_of_phd_completion=user_update["year_of_phd_completion"],
            ),
        )

    def get_user_details(
        self,
        user_id: int,
    ) -> Dict[str, Any]:
        """
        Returns the updated user details of a user.
        """
        stmt = text(
            """
SELECT  SL.SouthAfricanLegalStatus  AS legal_status,
        G.Gender                       AS gender,
        R.Race                         AS race,
        US.PhD                            AS has_phd,
        US.YearOfPhD                      AS year_of_phd
FROM UserStatistics US
    JOIN SouthAfricanLegalStatus SL ON US.SouthAfricanLegalStatus_Id = SL.SouthAfricanLegalStatus_Id
    JOIN Race R ON US.Race_Id = R.Race_Id
    JOIN Gender G ON US.Gender_Id = G.Gender_Id
WHERE US.PiptUser_Id = :user_id
                """
        )

        result = self.connection.execute(
            stmt,
            {
                "user_id": user_id,
            },
        )

        user = self.get(user_id)
        try:
            row = result.one()

            new_user_details = {
                "email": user.email,
                "given_name": user.given_name,
                "family_name": user.family_name,
                "legal_status": row["legal_status"],
                "gender": row["gender"],
                "race": row["race"],
                "has_phd": row["has_phd"],
                "year_of_phd_completion": row["year_of_phd"],
            }
        except NoResultFound:
            new_user_details = {
                "email": user.email,
                "given_name": user.given_name,
                "family_name": user.family_name,
                "legal_status": "Other",
                "gender": None,
                "race": None,
                "has_phd": None,
                "year_of_phd_completion": None,
            }

        return new_user_details

    def _update_username(self, user_id: int, new_username: str) -> None:
        """
        Updates the username of a user.
        """
        user = self.get(user_id)
        if new_username == user.username:
            return

        # Check that the new username isn't in use already
        if self._does_username_exist(new_username):
            raise ValueError(f"The username {new_username} exists already.")

        stmt = text(
            """
UPDATE PiptUser
SET Username = :new_username
WHERE PiptUser_Id = :user_id
        """
        )
        self.connection.execute(
            stmt, {"new_username": new_username, "user_id": user_id}
        )

    def is_investigator(self, username: str, proposal_code: str) -> bool:
        """
        Check whether a user is an investigator on a proposal.

        If the user or proposal do not exist, it is assumed the user is no investigator.
        """
        stmt = text(
            """
SELECT COUNT(*)
FROM ProposalCode PC
         JOIN ProposalInvestigator PI ON PC.ProposalCode_Id = PI.ProposalCode_Id
         JOIN Investigator I on PI.Investigator_Id = I.Investigator_Id
         JOIN PiptUser PU ON I.PiptUser_Id = PU.PiptUser_Id
WHERE PC.Proposal_Code = :proposal_code AND PU.Username = :username
        """
        )
        result = self.connection.execute(
            stmt, {"proposal_code": proposal_code, "username": username}
        )
        return cast(int, result.scalar_one()) > 0

    def is_principal_investigator(self, username: str, proposal_code: str) -> bool:
        """
        Check whether a user is the Principal Investigator of a proposal.

        If the user or proposal do not exist, it is assumed the user is no Principal
        Investigator.
        """
        stmt = text(
            """
SELECT COUNT(*)
FROM ProposalCode PCode
         JOIN ProposalContact PContact
                   ON PCode.ProposalCode_Id = PContact.ProposalCode_Id
         JOIN Investigator I ON PContact.Leader_Id = I.Investigator_Id
         JOIN PiptUser PU ON I.PiptUser_Id = PU.PiptUser_Id
WHERE PCode.Proposal_Code = :proposal_code AND PU.Username = :username
        """
        )
        result = self.connection.execute(
            stmt, {"proposal_code": proposal_code, "username": username}
        )
        return cast(int, result.scalar_one()) > 0

    def is_principal_contact(self, username: str, proposal_code: str) -> bool:
        """
        Check whether a user is the Principal Contact of a proposal.

        If the user or proposal do not exist, it is assumed the user is no Principal
        Contact.
        """
        stmt = text(
            """
SELECT COUNT(*)
FROM ProposalCode PCode
         JOIN ProposalContact PContact
                    ON PCode.ProposalCode_Id = PContact.ProposalCode_Id
         JOIN Investigator I ON PContact.Contact_Id = I.Investigator_Id
         JOIN PiptUser PU ON I.PiptUser_Id = PU.PiptUser_Id
WHERE PCode.Proposal_Code = :proposal_code AND PU.Username = :username
        """
        )
        result = self.connection.execute(
            stmt, {"proposal_code": proposal_code, "username": username}
        )
        return cast(int, result.scalar()) > 0

    def is_salt_astronomer(self, username: str) -> bool:
        """
        Check whether the user is a SALT Astronomer.

        If the user does not exist, it is assumed they are no SALT Astronomer.
        """
        stmt = text(
            """
SELECT COUNT(*)
FROM PiptUser PU
         JOIN PiptUserSetting PUS ON PU.PiptUser_Id = PUS.PiptUser_Id
         JOIN PiptSetting PS ON PUS.PiptSetting_Id = PS.PiptSetting_Id
WHERE PU.Username = :username
  AND PS.PiptSetting_Name = 'RightAstronomer'
  AND PUS.Value > 0
        """
        )
        result = self.connection.execute(stmt, {"username": username})
        return cast(int, result.scalar_one()) > 0

    def is_salt_operator(self, username: str) -> bool:
        """
        Check whether the user is a SALT Operator.

        If the user does not exist, it is assumed they are no SALT Operator.
        """
        stmt = text(
            """
SELECT COUNT(*)
FROM PiptUser PU
         JOIN PiptUserSetting PUS ON PU.PiptUser_Id = PUS.PiptUser_Id
         JOIN PiptSetting PS ON PUS.PiptSetting_Id = PS.PiptSetting_Id
WHERE PU.Username = :username
  AND PS.PiptSetting_Name = 'RightOperator'
  AND PUS.Value > 0
        """
        )
        result = self.connection.execute(stmt, {"username": username})
        return cast(int, result.scalar_one()) > 0

    def is_tac_member_for_proposal(self, username: str, proposal_code: str) -> bool:
        """
        Check whether the user is member of a TAC from which a proposal requests time.

        If the user or proposal do not exist, it is assumed the user is no TAC member.
        """
        stmt = text(
            """
SELECT COUNT(*)
FROM PiptUser PU
         JOIN PiptUserTAC PUT ON PU.PiptUser_Id = PUT.PiptUser_Id
         JOIN MultiPartner MP ON PUT.Partner_Id = MP.Partner_Id
         JOIN ProposalCode PC ON MP.ProposalCode_Id = PC.ProposalCode_Id
WHERE PC.Proposal_Code = :proposal_code
  AND MP.ReqTimePercent > 0
  AND Username = :username
        """
        )
        result = self.connection.execute(
            stmt, {"proposal_code": proposal_code, "username": username}
        )

        return cast(int, result.scalar_one()) > 0

    def is_tac_chair_for_proposal(self, username: str, proposal_code: str) -> bool:
        """
        Check whether the user is chair of a TAC from which a proposal requests time.

        If the user or proposal do not exist, it is assumed the user is no TAC chair.
        """
        stmt = text(
            """
SELECT COUNT(*)
FROM PiptUser PU
         JOIN PiptUserTAC PUT ON PU.PiptUser_Id = PUT.PiptUser_Id
         JOIN MultiPartner MP ON PUT.Partner_Id = MP.Partner_Id
         JOIN ProposalCode PC ON MP.ProposalCode_Id = PC.ProposalCode_Id
WHERE PC.Proposal_Code = :proposal_code
  AND MP.ReqTimePercent > 0
  AND PUT.Chair > 0
  AND Username = :username
        """
        )
        result = self.connection.execute(
            stmt, {"proposal_code": proposal_code, "username": username}
        )

        return cast(int, result.scalar_one()) > 0

    def is_tac_chair_in_general(self, username: str) -> bool:
        """
        Check whether the user is a TAC chair for any partner.

        If the user does not exist, it is assumed the user is no TAC chair.
        """
        stmt = text(
            """
SELECT COUNT(Username)
FROM PiptUserTAC PUT
    JOIN PiptUser PU ON PU.PiptUser_Id = PUT.PiptUser_Id
WHERE Username = :username
    AND PUT.Chair > 0
        """
        )
        result = self.connection.execute(stmt, {"username": username})

        return cast(int, result.scalar_one()) > 0

    def is_tac_member_in_general(self, username: str) -> bool:
        """
        Check whether the user is a TAC member for any partner.

        If the user does not exist, it is assumed the user is not a TAC member.
        """
        stmt = text(
            """
SELECT COUNT(Username)
FROM PiptUserTAC PUT
    JOIN PiptUser PU ON PU.PiptUser_Id = PUT.PiptUser_Id
WHERE Username = :username
        """
        )
        result = self.connection.execute(stmt, {"username": username})

        return cast(int, result.scalar_one()) > 0

    def is_board_member(self, username: str) -> bool:
        """
        Check whether the user is a SALT Board member.

        If the user does not exist, it is assumed they are no Board member.
        """
        stmt = text(
            """
SELECT COUNT(*)
FROM PiptUserSetting PUS
         JOIN PiptSetting PS ON PUS.PiptSetting_Id = PS.PiptSetting_Id
         JOIN PiptUser PU ON PUS.PiptUser_Id = PU.PiptUser_Id
WHERE PU.Username = :username
  AND PS.PiptSetting_Name = 'RightBoard'
  AND PUS.Value > 0;
        """
        )
        result = self.connection.execute(stmt, {"username": username})

        return cast(int, result.scalar_one()) > 0

    def is_partner_affiliated_user(self, username: str) -> bool:
        """
        Check whether the user is a user that is affiliated to a SALT partner.
        """
        stmt = text(
            """
SELECT COUNT(*)
FROM Investigator I
         JOIN PiptUser PU ON I.PiptUser_Id = PU.PiptUser_Id
         JOIN Institute I2 ON I.Institute_Id = I2.Institute_Id
         JOIN Partner P ON I2.Partner_Id = P.Partner_Id
WHERE PU.Username = :username
  AND P.Partner_Code != 'OTH'
  AND P.Virtual = 0;
        """
        )
        result = self.connection.execute(stmt, {"username": username})
        return cast(int, result.scalar_one()) > 0

    def is_administrator(self, username: str) -> bool:
        """
        Check whether the user is an administrator.

        If the user does not exist, it is assumed they are no administrator.
        """
        stmt = text(
            """
SELECT COUNT(*)
FROM PiptUser PU
    JOIN PiptUserSetting PUS ON PU.PiptUser_Id = PUS.PiptUser_Id
    JOIN PiptSetting PS ON PUS.PiptSetting_Id = PS.PiptSetting_Id
WHERE PS.PiptSetting_Name = 'RightAdmin'
    AND PUS.Value > 1
    AND PU.Username = :username
        """
        )
        result = self.connection.execute(stmt, {"username": username})
        return cast(int, result.scalar()) > 0

    def is_engineer(self) -> bool:
        """
        Should check whether the user is an engineer
        """
        # TODO Method need to be implemented.
        return False

    @staticmethod
    def get_password_hash(password: str) -> str:
        """Hash a plain text password."""
        return hashlib.md5(password.encode("utf-8")).hexdigest()  # nosec

    def _update_password_hash(self, username: str, password: str) -> None:
        new_password_hash = self.get_new_password_hash(password)
        stmt = text(
            """
INSERT INTO Password (Username, Password)
VALUES (:username, :password)
ON DUPLICATE KEY UPDATE Password = :password
        """
        )
        self.connection.execute(
            stmt, {"username": username, "password": new_password_hash}
        )

    def _does_user_id_exist(self, user_id: int) -> bool:
        stmt = text(
            """
SELECT COUNT(*) FROM PiptUser WHERE PiptUser_Id = :user_id
        """
        )
        result = self.connection.execute(stmt, {"user_id": user_id})

        return cast(int, result.scalar_one()) > 0

    def update_password(self, user_id: int, password: str) -> None:
        # TODO: Uncomment once the Password table exists.
        # self._update_password_hash(username, password)
        password_hash = self.get_password_hash(password)
        stmt = text(
            """
UPDATE PiptUser
SET Password = :password
WHERE PiptUser_Id = :user_id
        """
        )

        if not self._does_user_id_exist(user_id):
            raise NotFoundError(f"Unknown user id: {user_id}")

        self.connection.execute(stmt, {"user_id": user_id, "password": password_hash})

    def _update_user_details(self, user_id: int, user_update: Dict[str, str]) -> None:
        stmt = text(
            """
UPDATE Investigator 
SET FirstName = :given_name, 
    Surname = :family_name, 
    Email = :email
WHERE PiptUser_Id = :user_id
            """
        )

        try:
            self.connection.execute(
                stmt,
                {
                    "user_id": user_id,
                    "given_name": user_update["given_name"],
                    "family_name": user_update["family_name"],
                    "email": user_update["email"],
                },
            )

        except IntegrityError:
            raise NotFoundError(f"No such user id: {user_id}")

    @staticmethod
    def get_new_password_hash(password: str) -> str:
        """Hash a plain text password."""

        # Note that the type hint for the return value of the hash method is Any,
        # but the method is guaranteed to return a str.
        return cast(str, pwd_context.hash(password))

    def verify_password(self, password: str, hashed_password: str) -> bool:
        """Check a plain text password against a hash."""
        password_hash = self.get_password_hash(password)
        return secrets.compare_digest(password_hash, hashed_password)

    def find_user_with_username_and_password(
        self, username: str, password: str
    ) -> User:
        """
        Find a user with a username and password.

        If the combination of username and password is valid, then the corresponding
        user is returned. Otherwise a NotFoundError is raised.
        """
        user = self.get_by_username(username)
        if not user:
            raise NotFoundError()
        if not self.verify_password(password, user.password_hash):
            raise NotFoundError()

        return user

    def get_user_roles(self, username: str) -> List[Role]:
        """
        Get a user's roles.

        The roles do not include roles which are specific to a particular proposal (such
        as Principal Investigator). However, they include roles which are specific to a
        partner (i.e. TAC chair and member).
        """
        roles = []
        if self.is_administrator(username):
            roles.append(Role.ADMINISTRATOR)

        if self.is_salt_astronomer(username):
            roles.append(Role.SALT_ASTRONOMER)

        if self.is_board_member(username):
            roles.append(Role.BOARD_MEMBER)

        if self.is_tac_chair_in_general(username):
            roles.append(Role.TAC_CHAIR)

        if self.is_tac_member_in_general(username):
            roles.append(Role.TAC_MEMBER)

        return roles

    def get_salt_astronomers(self) -> List[Dict[str, Any]]:
        """
        Return the list of SALT Astronomers, sorted by family name.
        """
        stmt = text(
            """
SELECT
    I.PiptUser_Id          AS id,
    I.FirstName             AS given_name,
    I.Surname               AS family_name
FROM SaltAstronomers SA
    JOIN Investigator I ON SA.Investigator_Id = I.Investigator_Id
    ORDER BY I.Surname
        """
        )

        result = self.connection.execute(stmt)

        return [
            {
                "id": row.id,
                "given_name": row.given_name,
                "family_name": row.family_name,
            }
            for row in result
            if row.given_name != "Techops"
        ]

    def get_proposal_permissions(self, user_id: int) -> List[Dict[str, Any]]:
        """
        Return the list of proposal permissions which have been granted to a user.

        An error is raised if the user does not exist.
        """
        # Check that the user actually exists.
        if not self.is_existing_user_id(user_id):
            raise NotFoundError(f"No such user id: {user_id}")

        stmt = text(
            """
SELECT PC.Proposal_Code AS proposal_code, PP.ProposalPermission AS permission_type
FROM ProposalPermissionGrant PPG
         JOIN ProposalCode PC ON PPG.ProposalCode_Id = PC.ProposalCode_Id
         JOIN ProposalPermission PP
              ON PPG.ProposalPermission_Id = PP.ProposalPermission_Id
WHERE PPG.Grantee_Id = :grantee_id
        """
        )
        result = self.connection.execute(stmt, {"grantee_id": user_id})

        return [
            {"proposal_code": row.proposal_code, "permission_type": row.permission_type}
            for row in result
        ]

    def grant_proposal_permission(
        self, user_id: int, permission_type: str, proposal_code: str
    ) -> None:
        """
        Grant a proposal permission to a user.

        If the permission exists already, nothing is done and no error is raised.

        An error is raised if the passed username, permission type or proposal code
        doesn't exist.
        """
        # Check that the user actually exists.
        if not self.is_existing_user_id(user_id):
            raise NotFoundError(f"No such user id: {user_id}")

        # We could query for the ids in the insert statement, but that might give rise
        # to cryptic errors.
        permission_type_id = self._get_proposal_permission_type_id(permission_type)
        proposal_code_id = self._get_proposal_code_id(proposal_code)

        stmt = text(
            """
INSERT IGNORE INTO ProposalPermissionGrant (ProposalCode_Id,
                                            ProposalPermission_Id,
                                            Grantee_Id)
VALUES (:proposal_code_id, :permission_type_id, :grantee_id)
        """
        )
        self.connection.execute(
            stmt,
            {
                "permission_type_id": permission_type_id,
                "proposal_code_id": proposal_code_id,
                "grantee_id": user_id,
            },
        )

    def revoke_proposal_permission(
        self, user_id: int, permission_type: str, proposal_code: str
    ) -> None:
        """
        Revoke a proposal permission from a user.

        If the user does not have the permission, nothing is done and no error is
        raised.

        An error is raised if the passed username, permission type or proposal code
        doesn't exist.
        """
        # Check that the user actually exists.
        if not self.is_existing_user_id(user_id):
            raise NotFoundError(f"No such user id: {user_id}")

        # We could query for the ids in the insert statement, but that might give rise
        # to cryptic errors.
        permission_type_id = self._get_proposal_permission_type_id(permission_type)
        proposal_code_id = self._get_proposal_code_id(proposal_code)

        stmt = text(
            """
DELETE
FROM ProposalPermissionGrant
WHERE Grantee_Id = :grantee_id
  AND ProposalCode_Id = :proposal_code_id
  AND ProposalPermission_Id = :permission_type_id;
        """
        )
        self.connection.execute(
            stmt,
            {
                "grantee_id": user_id,
                "proposal_code_id": proposal_code_id,
                "permission_type_id": permission_type_id,
            },
        )

    def _get_proposal_permission_type_id(self, permission_type: str) -> int:
        stmt = text(
            """
SELECT ProposalPermission_Id
FROM ProposalPermission
WHERE ProposalPermission = :permission
        """
        )
        result = self.connection.execute(stmt, {"permission": permission_type})
        try:
            return cast(int, result.scalar_one())
        except NoResultFound:
            raise NotFoundError()

    def user_has_proposal_permission(
        self, user_id: int, permission_type: str, proposal_code: str
    ) -> bool:
        stmt = text(
            """
SELECT COUNT(*)
FROM ProposalPermissionGrant
WHERE Grantee_Id = :grantee_id
  AND ProposalCode_Id =
      (SELECT ProposalCode_Id FROM ProposalCode WHERE Proposal_Code = :proposal_code)
  AND ProposalPermission_Id = (SELECT ProposalPermission_Id
                               FROM ProposalPermission
                               WHERE ProposalPermission = :permission)
        """
        )
        result = self.connection.execute(
            stmt,
            {
                "grantee_id": user_id,
                "proposal_code": proposal_code,
                "permission": permission_type,
            },
        )

        return cast(int, result.scalar_one()) > 0

    def _get_proposal_code_id(self, proposal_code: str) -> int:
        stmt = text(
            """
SELECT ProposalCode_Id
FROM ProposalCode
WHERE Proposal_Code = :proposal_code
        """
        )
        result = self.connection.execute(stmt, {"proposal_code": proposal_code})
        try:
            return cast(int, result.scalar_one())
        except NoResultFound:
            raise NotFoundError()

    @staticmethod
    def _normalize_gender(gender: str) -> str:
        gender = gender.strip().lower()
        return gender[:1] + gender[1:]

    def _add_gender(self, gender: str) -> int:
        stmt = text(
            """
INSERT INTO Gender (Gender) VALUES (:gender)
            """
        )
        result = self.connection.execute(
            stmt, {"gender": self._normalize_gender(gender)}
        )
        return cast(int, result.lastrowid)

    def _get_gender_id(self, gender: str) -> int:
        stmt = text("""SELECT Gender_Id FROM Gender Where Gender = :gender""")
        result = self.connection.execute(
            stmt, {"gender": self._normalize_gender(gender)}
        )
        try:
            return cast(int, result.scalar_one())
        except NoResultFound:
            return self._add_gender(gender)

    def _add_race(self, race: str) -> int:
        stmt = text(
            """
INSERT INTO Race (Race) VALUES (:race)
            """
        )
        result = self.connection.execute(stmt, {"race": self._normalize_gender(race)})
        return cast(int, result.lastrowid)

    def _get_race_id(self, race: str) -> int:
        stmt = text("""SELECT Race_Id FROM Race Where Race = :race""")
        result = self.connection.execute(stmt, {"race": self._normalize_gender(race)})
        try:
            return cast(int, result.scalar_one())
        except NoResultFound:
            return self._add_race(race)

    def _get_legal_status_id(self, legal_status: str) -> int:
        stmt = text(
            """
SELECT SouthAfricanLegalStatus_Id
FROM SouthAfricanLegalStatus
Where SouthAfricanLegalStatus = :legal_status
            """
        )
        result = self.connection.execute(
            stmt, {"legal_status": self._normalize_gender(legal_status)}
        )
        return cast(int, result.scalar_one())

    def _update_user_statistics(
        self, pipt_user_id: int, user_information: Dict[str, Any]
    ) -> None:
        stmt = text(
            """
INSERT INTO UserStatistics (
                PiptUser_Id, 
                SouthAfricanLegalStatus_Id, 
                Gender_Id, 
                Race_Id, 
                PhD, 
                YearOfPhD
                )
VALUES (:pipt_user_id, :legal_status_id, :gender_id, :race_id, :has_phd, :year_of_phd )
ON DUPLICATE KEY UPDATE
    SouthAfricanLegalStatus_Id = :legal_status_id,
    Gender_Id = :gender_id,
    Race_Id = :race_id,
    PhD = :has_phd,
    YearOfPhD = :year_of_phd
            """
        )
        self.connection.execute(
            stmt,
            {
                "pipt_user_id": pipt_user_id,
                "legal_status_id": self._get_legal_status_id(
                    user_information["legal_status"]
                ),
                "gender_id": self._get_gender_id(user_information["gender"])
                if user_information["gender"]
                else None,
                "race_id": self._get_race_id(user_information["race"])
                if user_information["race"]
                else None,
                "has_phd": user_information["has_phd"],
                "year_of_phd": user_information["year_of_phd_completion"],
            },
        )
