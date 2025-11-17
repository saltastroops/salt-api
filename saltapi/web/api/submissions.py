import asyncio
from datetime import datetime, timedelta
from typing import Any, Dict, Optional

from fastapi import APIRouter, Depends, File, Form, Path, Query, UploadFile, WebSocket
from starlette import status

from saltapi.exceptions import AuthorizationError, NotFoundError
from saltapi.repository.database import engine
from saltapi.repository.submission_repository import SubmissionRepository
from saltapi.repository.unit_of_work import UnitOfWork
from saltapi.service.authentication_service import (
    find_user_from_token,
    get_current_user,
)
from saltapi.service.submission import SubmissionLogEntry, SubmissionStatus
from saltapi.service.user import User
from saltapi.web import services
from saltapi.web.schema.submissions import Submission, SubmissionProgress

router = APIRouter(prefix="/submissions", tags=["Submissions"])

TIME_BETWEEN_DB_QUERIES = 5

SUBMISSION_PROGRESS_TIMEOUT = timedelta(hours=5)


@router.post(
    "/",
    summary="Submit a proposal",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=Submission,
)
async def create_submission(
    proposal: UploadFile = File(
        ..., title="Proposal", description="Zip file containing the proposal"
    ),
    proposal_code: Optional[str] = Form(
        None, title="Proposal code", description="Proposal code"
    ),
    user: User = Depends(get_current_user),
) -> Dict[str, str]:
    """
    Submit a proposal.

    The proposal must be submitted as a zip file containing the XML file defining the
    whole proposal or the updated/added blocks, as well as the additional files such as
    finder charts.

    A proposal code may be passed as a query parameter. This is mandatory when blocks
    rather than a whole proposal are submitted. If a whole proposal is submitted and a
    proposal code is supplied as a query parameter, the proposal code defined in the
    proposal must be the same as that passed as a query parameter.
    """
    # Submissions don't use database transactions. As such no unit of work is used.
    # This can lead to warnings when mocking with the pytest-pymysql-autorecord plugin,
    # which you may ignore.
    connection = engine().connect().execution_options(isolation_level="AUTOCOMMIT")
    submission_repository = SubmissionRepository(connection)
    submission_service = services.submission_service(submission_repository)
    xml = await submission_service.extract_xml(proposal)

    # If a proposal code exists in the XML, the user must explicitly make a submission
    # for that proposal code.
    xml_proposal_code = submission_service.extract_proposal_code(xml)
    if xml_proposal_code and xml_proposal_code != proposal_code:
        raise ValueError(
            f"The proposal code specified by the query ({proposal_code} differs from "
            f"the proposal code in the submitted XML ({xml_proposal_code})."
        )

    if xml_proposal_code:
        proposal_code = xml_proposal_code

    # Check that the user is allowed to make the submission
    permission_service = services.permission_service(connection)
    permission_service.check_permission_to_submit_proposal(user, proposal_code)

    submission_identifier = await submission_service.submit_proposal(
        user, proposal, proposal_code
    )
    return {"submission_identifier": submission_identifier}


@router.get("/{identifier}/progress", response_model=SubmissionProgress)
async def get_submission_progress(
    identifier: str = Path(
        ...,
        title="Submission identifier",
        description="Unique identifier for the submission whose log is requested.",
    ),
    from_entry_number: int = Query(
        1,
        alias="from-entry-number",
        title="Minimum entry number",
        description=(
            "Minimum entry number from which onwards log entries are considered"
        ),
    ),
    user: User = Depends(get_current_user),
) -> Dict[str, Any]:
    """
    Get the progress information for a submission.

    The following details are returned for the submission with the given identifier:

    - The current submission status, which may be "Failed", "In progress" or
      "Successful".
    - The list of log entries. Each log entry consists of the time when it was logged
      (as an ISO 8601 datetime string), the type of log message ("Error", "Info" or
      "Warning") and the log message.
    - The proposal code, which may be None.

    By default, all the submission's log entries are returned. However, you may use the
    query parameter from-entry-number to request log entries starting from an entry
    number only. For example, if from-entry-number is 3, only the third, fourth, ...
    log entry are included in the response.
    """
    with UnitOfWork() as unit_of_work:
        submission_repository = SubmissionRepository(unit_of_work.connection)

        # Check that the authenticated user made the submission (and, implicitly, that
        # the identifier exists).
        submission = submission_repository.get(identifier)
        if submission["submitter_id"] != user.id:
            raise AuthorizationError(
                "You cannot access the submission log as someone else made the "
                "submission."
            )

        # Get the submission status and log entries
        submission_progress = submission_repository.get_progress(
            identifier=identifier,
            from_entry_number=from_entry_number,
        )

        # Datetimes cannot be serialized, so we convert them to ISO 8601 strings.
        for log_entry in submission_progress["log_entries"]:
            log_entry["logged_at"] = log_entry["logged_at"].isoformat()

        # Send a message with the current status, new log entries and proposal code.
        return submission_progress
