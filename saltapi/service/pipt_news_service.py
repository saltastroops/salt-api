from typing import Any, Dict, List

from saltapi.repository.pipt_news_repository import PiptNewsRepository


class PiptNewsService:
    def __init__(self, pipt_news_repository: PiptNewsRepository) -> None:
        self.pipt_news_repository = pipt_news_repository

    def get_news_for_days(self, days: int) -> List[Dict[str, Any]]:
        return self.pipt_news_repository.get_news_for_days(days)
