from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional


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


@dataclass(frozen=True)
class UserStatistics:
    legal_status: str
    gender: Optional[str]
    race: Optional[str]
    has_phd: Optional[bool]
    year_of_phd_completion: Optional[int]


@dataclass(frozen=True)
class NewUserDetails(UserStatistics):
    given_name: str
    family_name: str
    email: str
    username: str
    password: str
    institution_id: int


@dataclass(frozen=True)
class UserDetails(UserStatistics):
    given_name: str
    family_name: str
    email: str


@dataclass(frozen=True)
class UserUpdate(UserDetails):
    password: Optional[str]


class UserRight(str, Enum):
    HOME_NEWS = "HomeNews"
    HOME_PROPOSALS = "HomeProposals"
    MASK_CUTTING = "RightMaskCutting"
    HOME_NEWS_ENTRIES = "HomeNewsEntries"
    EDIT_NIGHT_LOG = "RightEditNightLog"
    VIEW_NIGHT_LOG = "RightViewNightLog"
    HOME_WEATHER_INFORMATION = "HomeWeatherInformation"
    HOME_PROPOSAL_STATS = "HomeProposalStatistics"
    FABRY_PEROT_SCIENTIST = "RightFabryPerotScientist"

    @property
    def display_name(self) -> str:
        return DISPLAY_NAMES[self]


DISPLAY_NAMES: Dict[UserRight, str] = {
    UserRight.HOME_NEWS: "Home News",
    UserRight.HOME_PROPOSALS: "Home Proposals",
    UserRight.MASK_CUTTING: "Mask Cutting",
    UserRight.HOME_NEWS_ENTRIES: "Home News Entries",
    UserRight.EDIT_NIGHT_LOG: "Edit Night Log",
    UserRight.VIEW_NIGHT_LOG: "View Night Log",
    UserRight.HOME_WEATHER_INFORMATION: "Home Weather Information",
    UserRight.HOME_PROPOSAL_STATS: "Home Proposal Statistics",
    UserRight.FABRY_PEROT_SCIENTIST: "Fabry-Perot Scientist",
}
