from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field

from saltapi.web.schema.common import ProposalCode
from saltapi.web.schema.institution import UserInstitution


class UserRole(str, Enum):
    """
    User roles.

    In case of TAC members and chairs the role means that the user is a TAC member or
    chair for any (but not all) of the SALT partners.

    The administrator role refers to being an administrator for the API.
    """

    SALT_ASTRONOMER = "SALT Astronomer"
    SALT_OPERATOR = "SALT Operator"
    ADMINISTRATOR = "Administrator"
    ENGINEER = "Engineer"
    TAC_MEMBER = "TAC Member"
    TAC_CHAIR = "TAC Chair"
    BOARD_MEMBER = "Board Member"
    LIBRARIAN = "Librarian"


class FullName(BaseModel):
    given_name: str = Field(..., title="Given name", description='Given ("first") name')
    family_name: str = Field(
        ..., title="Family name", description='Family ("last") name'
    )

    class Config:
        orm_mode = True


class UserListItem(FullName):
    """Item in a list of users."""

    id: int = Field(..., title="User id", description="User id.")
    username: str = Field(..., title="Username", description="The username.")


class LegalStatus(str, Enum):
    """
    South African legal status.
    """

    SOUTH_AFRICAN_CITIZEN = "South African citizen"
    PERMANENT_RESIDENT_OF_SOUTH_AFRICA = "Permanent resident of South Africa"
    OTHER = "Other"


class UserDemographics(BaseModel):
    """The User statistics."""

    legal_status: LegalStatus = Field(
        ..., title="Legal status", description="The legal status in South Africa"
    )
    gender: Optional[str] = Field(..., title="Gender", description="Gender.")
    race: Optional[str] = Field(..., title="Race", description="Race.")
    has_phd: Optional[bool] = Field(
        ..., title="PhD", description="Does the user has a PhD?"
    )
    year_of_phd_completion: Optional[int] = Field(
        None,
        title="Year of PhD degree completion",
        description="The year the PhD degree was completed",
    )


class User(FullName):
    """User details."""

    id: int = Field(..., title="User id", description="User id.")
    email: EmailStr = Field(..., title="Email address", description="Email address")
    username: str = Field(..., title="Username", description="Username.")
    roles: List[UserRole] = Field(..., title="User roles", description="User roles.")
    affiliations: List[UserInstitution] = Field(
        ..., title="Affiliation", description="Affiliation of the user"
    )
    demographics: Optional[UserDemographics] = Field(
        None,
        title="User Demographics",
        description="Information about user's legal status in South Africa",
    )


class BaseUserDetails(BaseModel):
    """
    Details for creating/updating a user.
    """

    given_name: str = Field(..., title="Given name", description="Given name.")
    family_name: str = Field(..., title="Family name", description="Family name.")
    email: str = Field(..., title="Email", description="Email.")
    legal_status: LegalStatus = Field(
        ..., title="Legal status", description="The legal status in South Africa"
    )
    gender: Optional[str] = Field(..., title="Gender", description="Gender.")
    race: Optional[str] = Field(..., title="Race", description="Race.")
    has_phd: Optional[bool] = Field(
        ..., title="PhD", description="Does the user has a PhD?"
    )
    year_of_phd_completion: Optional[int] = Field(
        None,
        title="Year of PhD degree completion",
        description="The year the PhD degree was completed",
    )


class NewUserDetails(BaseUserDetails):
    """Details for creating a user."""

    username: str = Field(..., title="Username", description="Username.")
    password: str = Field(..., title="Password", description="Password.")
    institution_id: int = Field(
        ...,
        title="Institution id",
        description=(
            "Unique identifier of the institution to which the user is affiliated."
        ),
    )


class UserUpdate(BaseUserDetails):
    """
    Details for updating a user.
    """

    password: Optional[str] = Field(None, title="Password", description="Password.")


class PasswordResetRequest(BaseModel):
    """Username or email address for which a password reset is requested."""

    username_email: str = Field(
        ...,
        title="Username or email",
        description=(
            "Username or email address of the user whose password should be reset"
        ),
    )


class UserSwitchDetails(BaseModel):
    """Username of the user to switch to."""

    username: str = Field(
        ..., title="Username", description="Username of the user to switch to"
    )


class ProposalPermissionType(str, Enum):
    """Proposal permission type."""

    VIEW = "View"


class ProposalPermission(BaseModel):
    """A permission for a specific proposal."""

    permission_type: ProposalPermissionType = Field(
        ..., title="Proposal permission type", description="Proposal permission type"
    )
    proposal_code: ProposalCode = Field(
        ...,
        title="Proposal code",
        description="Proposal code to which the permission applies",
    )


class UserId(BaseModel):
    """A user id."""

    id: Optional[int] = Field(..., title="User id", description="A user id.")


class SaltAstronomer(FullName):
    """The SALT Astronomers."""

    id: int = Field(..., title="User id", description="User id.")


class PasswordUpdate(BaseModel):
    password: str = Field(..., title="Password", description="Password.")
    authentication_key: str = Field(
        ..., title="Authentication token", description="The authentication Token"
    )


class UsernameEmail(BaseModel):
    username_email: str = Field(
        ..., title="Username or Email", description="Username or Email."
    )


class UserContact(BaseModel):
    email: str = Field(..., title="Email address", description="The email address.")
    institution_id: int = Field(
        ...,
        title="Institution id",
        description=(
            "Unique identifier of the institution to which the user is affiliated."
        ),
    )


class SubscriptionType(str, Enum):
    """
    The type of subscriptions a user can subscribe to
    """

    SALT_NEWS = "SALT News"
    GRAVITATIONAL_WAVE_News = "Gravitational Wave Notifications"


class Subscription(BaseModel):
    to: SubscriptionType = Field(
        ..., title="Subscription", description="The type of the subscription."
    )
    is_subscribed: bool = Field(
        ..., title="Is subscribed", description="Whether the user is subscribed"
    )


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


class UserRightStatus(BaseModel):
    """Represents a user right and its current status."""

    right: UserRight = Field(
        ...,
        title="Right name",
        description="The display name of the user right (e.g. 'Edit Night Log').",
    )
    is_granted: bool = Field(
        ...,
        title="Granted",
        description="Whether the user currently has this right (true) or not (false).",
    )
