import pytest
from sqlalchemy.engine import Connection

from saltapi.exceptions import NotFoundError
from saltapi.repository.pipt_news_repository import PiptNewsRepository
from tests.markers import nodatabase


@nodatabase
def test_get_news_for_last_370_days_returns_data(
    db_connection: Connection, check_data
) -> None:
    repo = PiptNewsRepository(db_connection)
    news = repo.get_news_for_days(370)
    check_data(news)


@nodatabase
def test_get_news_for_today_raises_not_found(db_connection: Connection) -> None:
    repo = PiptNewsRepository(db_connection)

    with pytest.raises(NotFoundError) as excinfo:
        repo.get_news_for_days(0)
    assert "No news items found" in str(excinfo.value)
