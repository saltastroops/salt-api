from typing import Any, Dict, List

from sqlalchemy import text
from sqlalchemy.engine import Connection

from saltapi.exceptions import NotFoundError


class PiptNewsRepository:
    def __init__(self, connection: Connection) -> None:
        self.connection = connection

    def get_news_for_days(self, days: int) -> List[Dict[str, Any]]:
        """
        Returns a list of PIPT news entries issued within the last `days` days.
        """
        stmt = text(
            """
            SELECT Time AS time, Title AS title, Text AS text
            FROM PiptNews
            WHERE DATE_SUB(CURDATE(), INTERVAL :days DAY) <= Time
            ORDER BY Time DESC
            """
        )

        result = self.connection.execute(stmt, {"days": days})
        news_items = [
            {
                "date": row.time.strftime("%a, %d %b %Y %H:%M:%S"),
                "title": row.title,
                "text": row.text,
            }
            for row in result
        ]
        if not news_items:
            raise NotFoundError(f"No news items found in the last {days} day(s).")
        return news_items
