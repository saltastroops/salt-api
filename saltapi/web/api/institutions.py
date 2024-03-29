from typing import Any, Dict, List

from fastapi import APIRouter, Body, HTTPException
from starlette import status

from saltapi.exceptions import ResourceExistsError
from saltapi.repository.unit_of_work import UnitOfWork
from saltapi.service.institution import Institution as _NewInstitutionDetails
from saltapi.web import services
from saltapi.web.schema.institution import Institution, NewInstitutionDetails

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


@router.post(
    "/",
    summary="Create an institution",
    status_code=status.HTTP_201_CREATED,
)
def create_institution(
    institution: NewInstitutionDetails = Body(
        ...,
        title="Institution details",
        description="Institution details for the institution to create.",
    )
) -> _NewInstitutionDetails:
    with UnitOfWork() as unit_of_work:
        institution_service = services.institution_service(unit_of_work.connection)
        try:
            institution_service.create(institution.dict())

            unit_of_work.commit()
        except ResourceExistsError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The institution exists already.",
            )

        return institution_service.get_institution_by_name_and_department(
            institution.institution_name, institution.department
        )
