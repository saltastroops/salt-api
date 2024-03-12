from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class Status(str, Enum):
    AVAILABLE = "Available"
    AVAILABLE_WITH_RESTRICTIONS = "Available with restrictions"
    UNAVAILABLE = "Unavailable"


class SubsystemStatus(BaseModel):
    expected_available_again_at: Optional[datetime] = Field(
        ...,
        title="Time when expected available again",
        description="Date time when the subsystem is expected to be available again, as an ISO 8601 string",
    )
    reason: Optional[str] = Field(
        ...,
        title="Reason for the status",
        description="Reason for the status.",
    )
    reporting_user: str = Field(
        ...,
        title="Reporting user",
        description="Name of the user reporting this status update",
    )
    status: Status = Field(..., title="Status", description="Status")
    status_changed_at: datetime = Field(
        ...,
        title="Time of status change",
        description="Date and time when the status changed, as an ISO 8601 string.",
    )
    subsystem: str = Field(
        ...,
        title="Telescope subsystem",
        description='Telescope subsystem, such as "Telescope" or "RSS"',
    )


class SubsystemStatusUpdate(BaseModel):
    expected_available_again_at: Optional[datetime] = Field(
        ...,
        title="Time when expected available again",
        description="Date time when the subsystem is expected to be available again, as an ISO 8601 string",
    )
    reason: Optional[str] = Field(
        ...,
        title="Reason for the status",
        description="Reason for the status. This must be None if the subsystem is available.",
    )
    reporting_user: str = Field(
        ...,
        title="Reporting user",
        description="Name of the user reporting this status update",
    )
    status: Status = Field(..., title="Status", description="Status")
    status_changed_at: Optional[datetime] = Field(
        ...,
        title="Time of status change",
        description="Date and time when the status changed, as an ISO 8601 string. This may be None if the status has not changed.",
    )
    subsystem: str = Field(
        ...,
        title="Telescope subsystem",
        description='Telescope subsystem, such as "Telescope" or "RSS"',
    )
