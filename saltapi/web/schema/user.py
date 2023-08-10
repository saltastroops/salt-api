from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field

from saltapi.web.schema.common import ProposalCode
from saltapi.web.schema.institution import Institution


class UserRole(str, Enum):
    """
    User roles.

    In case of TAC members and chairs the role means that the user is a TAC member or
    chair for any (but not all) of the SALT partners.

    The administrator role refers to being an administrator for the API.
    """

    SALT_ASTRONOMER = "SALT Astronomer"
    ADMINISTRATOR = "Administrator"
    TAC_MEMBER = "TAC Member"
    TAC_CHAIR = "TAC Chair"
    BOARD_MEMBER = "Board Member"


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


class User(FullName):
    """User details."""

    id: int = Field(..., title="User id", description="User id.")
    email: EmailStr = Field(..., title="Email address", description="Email address")
    alternative_emails: List[EmailStr] = Field(
        ...,
        title="Alternative email addresses",
        description="Alternative email addresses",
    )
    username: str = Field(..., title="Username", description="Username.")
    roles: List[UserRole] = Field(..., title="User roles", description="User roles.")
    affiliations: List[Institution] = Field(
        ..., title="Affiliation", description="Affiliation of the user"
    )


class LegalStatus(str, Enum):
    """
    South African legal status.
    """

    SOUTH_AFRICAN_CITIZEN = "South African citizen"
    PERMANENT_RESIDENT_OF_SOUTH_AFRICA = "Permanent resident of South Africa"
    OTHER = "Other"


class UserStatistics(BaseModel):
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
        ...,
        title="Year of PhD degree completion",
        description="The year the PhD degree was completed",
    )


class NewUserDetails(FullName, UserStatistics):
    """Details for creating a user."""

    email: EmailStr = Field(..., title="Email address", description="Email address")
    username: str = Field(..., title="Username", description="Username.")
    password: str = Field(..., title="Password", description="Password.")
    institution_id: int = Field(
        ...,
        title="Institution id",
        description=(
            "Unique identifier of the institution to which the user is affiliated."
        ),
    )


class UserUpdate(UserStatistics):
    """
    New user details.

    A None value means that the existing value should be kept.
    """

    username: Optional[str] = Field(None, title="Username", description="Username.")
    given_name: Optional[str]
    family_name: Optional[str]
    email: Optional[str]
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
