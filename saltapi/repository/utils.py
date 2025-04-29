from typing import List
from sqlalchemy import text
from sqlalchemy.engine import Connection


class Utils:
    def __init__(self, connection: Connection) -> None:
        self.connection = connection

    def all_partners(self) -> List[str]:

        stmt = text(
        """
SELECT Partner_Code AS partner_code 
FROM Partner P
WHERE P.Partner_Code != 'OTH' AND P.Virtual = 0
        """
        )
        result = self.connection.execute(stmt)

        return [row.partner_code for row in result]