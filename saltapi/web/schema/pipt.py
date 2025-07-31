from datetime import datetime
from pydantic import BaseModel, EmailStr, Field
from typing import List, Literal, Optional
from saltapi.web.schema.institution import UserInstitution
from saltapi.web.schema.proposal import ProposalStatus, TimeAllocation
from saltapi.web.schema.common import ProposalCode


class PiptNewsItem(BaseModel):
    """A PIPT news item."""

    date: datetime = Field(
        ..., title="Date", description="Date and time of the news item"
    )
    title: str = Field(..., title="Title", description="Title of the news item")
    text: str = Field(..., title="Text", description="Content of the news item")


class PiptUserInfo(BaseModel):
    given_name: str = Field(..., title="First Name")
    family_name: str = Field(..., title="Last Name")
    email: EmailStr = Field(..., title="Email address", description="Email address")
    affiliations: List[UserInstitution] = Field(
        ..., title="Affiliation", description="Affiliation of the user"
    )


class PiptProposalInfo(BaseModel):
    proposal_code: ProposalCode = Field(
        ..., title="Proposal code", description="Proposal code"
    )
    title: str = Field(..., title="Title", description="Proposal title")
    phase: Literal[1, 2] = Field(
        ...,
        title="Proposal phase",
        description="Proposal phase",
    )
    status: ProposalStatus = Field(
        ..., title="Proposal status", description="Proposal status"
    )
    proposal_file: str = Field(
        ...,
        title="Proposal file",
        description=(
            "URL of the proposal file that can be imported into the Principal "
            "Investigator Proposal Tool"
        ),
    )
    time_allocations: List[TimeAllocation] = Field(
        ...,
        title="Time allocations",
        description="Time allocations for the semester",
    )


class ProposalConstraint(BaseModel):
    year: int = Field(..., title="Year", description="Year of the semester")
    semester: int = Field(..., title="Semester", description="Semester number")
    priority: int = Field(..., title="Priority", description="Proposal priority")
    moon: Optional[str] = Field(
        None, title="Moon Phase", description="Moon phase or name (optional)"
    )
    allocated_time: float = Field(
        ..., title="Allocated Time", description="Time allocated"
    )
