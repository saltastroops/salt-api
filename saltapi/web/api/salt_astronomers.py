from typing import Any, Dict, List

from fastapi import APIRouter
from saltapi.repository.unit_of_work import UnitOfWork
from saltapi.web import services
from saltapi.web.schema.user import UserListItem

router = APIRouter(prefix="/salt-astronomers", tags=["SALT Astronomers"])

@router.get(
    "/",
    summary="Get the SALT astronomers",
    response_model=List[UserListItem],
)
def get_salt_astronomers() -> List[Dict[str, Any]]:
    with UnitOfWork() as unit_of_work:
        user_service = services.user_service(unit_of_work.connection)
        return user_service.get_salt_astronomers()
