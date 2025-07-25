from typing import Any, Dict, List

from fastapi import APIRouter, HTTPException, Query
from starlette import status

from saltapi.exceptions import NotFoundError
from saltapi.repository.unit_of_work import UnitOfWork
from saltapi.web import services
from saltapi.web.schema.news import PiptNewsItem

router = APIRouter(prefix="/pipt-news", tags=["PIPT News"])


@router.get(
    "/",
    summary="Get PIPT news entries from the last N days",
    response_model=List[PiptNewsItem],
)
def get_pipt_news(
    days: int = Query(7, ge=1, description="Number of days to look back")
) -> List[Dict[str, Any]]:
    with UnitOfWork() as unit_of_work:
        service = services.pipt_news_service(unit_of_work.connection)
        try:
            return service.get_news_for_days(days)
        except NotFoundError as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e),
            )
