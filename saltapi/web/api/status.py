from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from starlette import status

router = APIRouter(prefix="", tags=["Status"])


@router.post("/status-update", summary="Update a SALT subsystem status")
def update_status(request: Request):
    host = request.client.host
    if not host or host[:4] not in ("10.1", "10.2"):
        return JSONResponse(
            {"message": "You may only update the status from within the SAAO network."},
            status_code=status.HTTP_403_FORBIDDEN,
        )
