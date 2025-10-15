from dataclasses import dataclass
from enum import Enum
from typing import List, Optional


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
    LIBRARIAN = "Librarian"
    MASK_CUTTER = "Mask Cutter"


@dataclass()
class ContactDetails:
    given_name: str
    family_name: str
    email: str


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
    email: str


@dataclass()
class Institution:
    institution_id: int
    institution: str
    department: Optional[str]
    partner_code: str


@dataclass()
class UserDemographics:
    legal_status: str
    gender: Optional[str]
    race: Optional[str]
    has_phd: Optional[bool]
    year_of_phd_completion: int


@dataclass()
class User:
    id: int
    given_name: str
    family_name: str
    email: str
    username: str
    password_hash: str
    affiliations: List[Institution]
    roles: List[Role]
    user_verified: bool
    active: bool
    demographics: Optional[UserDemographics]


@dataclass(frozen=True)
class UserDemographics:
    legal_status: str
    gender: Optional[str]
    race: Optional[str]
    has_phd: Optional[bool]
    year_of_phd_completion: Optional[int]


@dataclass(frozen=True)
class NewUserDetails(UserDemographics):
    given_name: str
    family_name: str
    email: str
    username: str
    password: str
    institution_id: int


@dataclass(frozen=True)
class UserDetails(UserDemographics):
    given_name: str
    family_name: str
    email: str


@dataclass(frozen=True)
class UserUpdate(UserDetails):
    password: Optional[str]
