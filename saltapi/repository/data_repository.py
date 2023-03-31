from typing import List, cast

from sqlalchemy import text
from sqlalchemy.engine import Connection

from saltapi.repository.block_repository import BlockRepository
from saltapi.repository.proposal_repository import ProposalRepository
from saltapi.exceptions import NotFoundError, ValidationError


class DataRepository:
    def __init__(self, connection: Connection) -> None:
        self.connection = connection
        self.proposal_repository = ProposalRepository(connection)
        self.block_repository = BlockRepository(connection)

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
            raise NotFoundError(f"Couldn't find requested data format '{data_format}'")

        return cast(int, data_format_id[0])

    def request_data(
        self,
        user_id: int,
        proposal_code: str,
        observation_ids: List[int],
        data_formats: List[str],
    ):
        """
        Create an observation data request.
        """
        try:
            proposal_code_id = self.proposal_repository.get_proposal_code_id(
                proposal_code
            )
        except NotFoundError:
            raise ValidationError(f"Couldn't find  proposal code '{proposal_code}'")

        block_visit_ids = [
            o["id"] for o in self.proposal_repository.block_visits(proposal_code)
        ]
        for o in observation_ids:
            if o not in block_visit_ids:
                raise ValidationError(
                    f"You can not request observation id '{o}' for proposal code: '{proposal_code}'"
                )

        insert_rows = []
        for data_format in data_formats:
            if data_format == "All":
                data_format_id = self._get_data_format_id("all")
                for block_visit_id in observation_ids:
                    insert_rows.append(
                        {
                            "proposal_code_id": proposal_code_id,
                            "block_visit_id": block_visit_id,
                            "user_id": user_id,
                            "data_format_id": data_format_id,
                        }
                    )
            elif data_format == "Calibration":
                insert_rows.append(
                    {
                        "proposal_code_id": proposal_code_id,
                        "block_visit_id": None,
                        "user_id": user_id,
                        "data_format_id": self._get_data_format_id("calibration"),
                    }
                )
            else:
                raise ValidationError(f"Data format '{data_format}' is not supported.")
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
VALUES (
    :proposal_code_id,
    :block_visit_id,
    :user_id,
    :data_format_id,
    0,
    NOW()
)
        """
        )
        self.connection.execute(
            stmt,
            insert_rows,
        )
