from typing import List, cast

from sqlalchemy import text
from sqlalchemy.engine import Connection

from saltapi.repository.proposal_repository import ProposalRepository
from saltapi.exceptions import NotFoundError


class DataRepository:
    def __init__(self, connection: Connection) -> None:
        self.connection = connection
        self.proposal_repository = ProposalRepository(connection)

    def _get_data_format_id(self, data_format: str):
        stmt = text(
            """
SELECT RequestDataFormat_Id FROM RequestDataFormat
WHERE RequestDataFormat = :data_format
        """
        )
        result = self.connection.execute(stmt, {"data_format": data_format})
        data_format_id = result.one_or_none()
        if not data_format_id:
            raise NotFoundError(f"Couldn't find  requested data format `{data_format}`")

        return cast(int, data_format_id[0])

    def request_observations(
        self,
        user_id: int,
        proposal_code: str,
        block_visits_ids: List[int],
        data_formats: List[str],
    ):
        """
        Create a observations data request
        """
        proposal_code_id = self.proposal_repository.get_proposal_code_id(proposal_code)
        data_format_id = self._get_data_format_id("all")
        insert_rows = []
        for b in block_visits_ids:
            insert_rows.append(
                {
                    "proposal_code_id": proposal_code_id,
                    "block_visit_id": b,
                    "user_id": user_id,
                    "data_format_id": data_format_id,
                }
            )
        if "calibration" in data_formats:
            insert_rows.append(
                {
                    "proposal_code_id": proposal_code_id,
                    "block_visit_id": None,
                    "user_id": user_id,
                    "data_format_id": self._get_data_format_id("calibration"),
                }
            )
        stmt = text(
            """
INSERT INTO RequestData (
    ProposalCode_Id,
    BlockVisit_Id,
    PiptUser_Id,
    RequestDataFormat_Id,
    Complete,
    RequestDate
)
VALUES(
    :proposal_code_id,
    :block_visit_id,
    :user_id,
    :data_format_id,
    0,
    NOW()
)
        """
        )
        result = self.connection.execute(
            stmt,
            insert_rows,
        )

        if not result.rowcount:
            raise NotFoundError()
