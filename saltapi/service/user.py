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
    HOME_NEWS = "Home News"
    HOME_PROPOSALS = "Home Proposals"
    MASK_CUTTING = "Mask Cutting"
    HOME_NEWS_ENTRIES = "Home News Entries"
    EDIT_NIGHT_LOG = "Edit Night Log"
    VIEW_NIGHT_LOG = "View Night Log"
    HOME_WEATHER_INFORMATION = "Home Weather Information"
    HOME_PROPOSAL_STATS = "Home Proposal Statistics"
    FABRY_PEROT_SCIENTIST = "Fabry-Perot Scientist"


RIGHT_DB_NAMES: Dict[UserRight, str] = {
    UserRight.HOME_NEWS: "HomeNews",
    UserRight.HOME_PROPOSALS: "HomeProposals",
    UserRight.MASK_CUTTING: "RightMaskCutting",
    UserRight.HOME_NEWS_ENTRIES: "HomeNewsEntries",
    UserRight.EDIT_NIGHT_LOG: "RightEditNightLog",
    UserRight.VIEW_NIGHT_LOG: "RightViewNightLog",
    UserRight.HOME_WEATHER_INFORMATION: "HomeWeatherInformation",
    UserRight.HOME_PROPOSAL_STATS: "HomeProposalStatistics",
    UserRight.FABRY_PEROT_SCIENTIST: "RightFabryPerotScientist",
}
