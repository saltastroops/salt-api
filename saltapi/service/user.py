from dataclasses import dataclass
from enum import Enum
from typing import List, NamedTuple, Optional


class Role(str, Enum):
    SALT_ASTRONOMER = "SALT Astronomer"
    SALT_OPERATOR = "SALT Operator"
    ADMINISTRATOR = "Administrator"
    TAC_MEMBER = "TAC Member"
    TAC_CHAIR = "TAC Chair"
    BOARD_MEMBER = "Board Member"
    ENGINEER = "Engineer"
    PRINCIPAL_CONTACT = "Principal Contact"
    PRINCIPAL_INVESTIGATOR = "Principal Investigator"
    INVESTIGATOR = "Investigator"
    PROPOSAL_TAC_MEMBER = "Proposal TAC Member"
    PROPOSAL_TAC_CHAIR = "Proposal TAC Chair"
    PARTNER_AFFILIATED = "Partner Affiliated"


@dataclass()
class ContactDetails:
    given_name: str
    family_name: str
    email: str
    alternative_emails: List[str]


@dataclass()
class UserListItem:
    id: int
    family_name: str
    given_name: str

@dataclass()
class LiaisonAstronomer:
    id: int
    family_name: str
    given_name: str

@dataclass()
class Institution:
    institution_id: int
    institution: str
    department: Optional[str]
    partner_code: str


@dataclass()
class User:
    id: int
    given_name: str
    family_name: str
    email: str
    alternative_emails: List[str]
    username: str
    password_hash: str
    affiliations: List[Institution]
    roles: List[Role]


@dataclass()
class NewUserDetails:
    given_name: str
    family_name: str
    email: str
    alternative_emails: List[str]
    username: str
    password: str
    institution_id: int


class UserUpdate(NamedTuple):
    username: Optional[str]
    # Not implemented yet
    # given_name: Optional[str]
    # family_name: Optional[str]
    # email: Optional[str]
    password: Optional[str]
