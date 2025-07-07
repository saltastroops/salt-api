from enum import Enum
from typing import List, Optional

from pydantic import UUID4, BaseModel, Field


class Submission(BaseModel):
    """A proposal submission."""

    submission_identifier: UUID4 = Field(
        ...,
        title="Submission identifier",
        description="Unique identifier for the submission",
    )


class SubmissionStatus(str, Enum):
    """Submission status value."""

    FAILED = "Failed"
    IN_PROGRESS = "In progress"
    SUCCESSFUL = "Successful"


class SubmissionMessageType(str, Enum):
    ERROR = "Error"
    INFO = "Info"
    WARNING = "Warning"


class SubmissionLogEntry(BaseModel):
    """A submission log entry."""

    entry_number: int = Field(
        ...,
        title="Log entry number",
        description=(
            "The running number, starting at 1, for the log entries associated with the"
            " submission."
        ),
    )
    logged_at: str = Field(
        ...,
        title="Datetime when logged",
        description="The datetime when this entry was logged, as an ISO 8601 string.",
    )
    message_type: SubmissionMessageType = Field(
        ..., title="Log message type.", description="The type of log message."
    )
    message: str = Field(..., title="Log message", description="The log message.")


class SubmissionProgress(BaseModel):
    status: SubmissionStatus = Field(
        ..., title="Submission status", description="The submission status"
    )
    log_entries: List[SubmissionLogEntry] = Field(
        ..., title="Log entries.", description="The list of log entries."
    )
    proposal_code: Optional[str] = Field(
        ..., title="Proposal code", description="The proposal code."
    )
