from typing import Any, Dict, List

from fastapi import APIRouter

from saltapi.repository.unit_of_work import UnitOfWork
from saltapi.web import services
from saltapi.web.schema.institution import Institution

router = APIRouter(prefix="/institutions", tags=["Institutions"])


@router.get(
    "/",
    summary="Get a list of institutions",
    response_model=List[Institution],
)
def get_institutions() -> List[Dict[str, Any]]:
    with UnitOfWork() as unit_of_work:
        institution_service = services.institution_service(unit_of_work.connection)
        return institution_service.get_institutions()
