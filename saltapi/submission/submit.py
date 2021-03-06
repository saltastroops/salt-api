"""Submit proposal content."""
import os
from typing import Optional

import httpx
from starlette.datastructures import UploadFile

from saltapi.auth.token import create_token
from saltapi.repository.user_repository import User
import logging

logger = logging.getLogger(__name__)

proposal_submission_url = f"{os.environ['STORAGE_SERVICE_URL']}/proposal/submit"


async def submit_proposal(
    proposal: UploadFile, proposal_code: Optional[str], submitter: str
) -> str:
    """Submit a proposal."""
    generic_error = "The proposal could not be sent to the storage service."
    files = {
        "proposal": (proposal.filename, proposal.file, "application/octet-stream"),
    }
    data = {
        "submitter": submitter,
    }
    if proposal_code:
        data["proposal_code"] = proposal_code
    user = User(
        id=-1,
        username="admin",
        first_name="",
        last_name="",
        email="",
        roles=["Admin"],
        permissions=[],
    )
    auth_token = create_token(user=user, expiry=300, algorithm="RS256")
    headers = {"Authorization": f"Bearer {auth_token}"}
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                proposal_submission_url, data=data, files=files, headers=headers
            )
    except Exception:
        logger.exception(msg=generic_error)
        raise Exception(generic_error)
    submission_id = _submission_id(response)
    if submission_id:
        return submission_id

    # error handling
    error = _submission_error(response)
    if error:
        logger.error(msg=error)
        raise Exception(error)
    else:
        logger.error(msg=generic_error)
        raise Exception(generic_error)


def _submission_id(response: httpx.Response) -> Optional[str]:
    """
    Extract the submission id sent by the server, if there is one.

    The response body is parsed as a JSON object and its submission_id field is
    returned. If this fails (because the response isn't JSON object or has no
    submission_id field) None is returned.
    """
    try:
        submission_id = response.json().get("submission_id")
        if submission_id is not None:
            return str(submission_id)
        else:
            return None
    except Exception:
        return None


def _submission_error(response: httpx.Response) -> Optional[str]:
    """
    Extract the error message sent by the server, if there is one.

    The response body and is parsed as a JSON object and its error field is returned.
    If this fails (because the response isn't JSON object or has no error field) None is
    returned.
    """
    try:
        error = response.json().get("error")
        if error is not None:
            return str(error)
        else:
            return None
    except Exception:
        return None
