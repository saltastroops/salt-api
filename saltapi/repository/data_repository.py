from typing import Any, Dict, List, cast

from sqlalchemy import text
from sqlalchemy.engine import Connection

from saltapi.exceptions import NotFoundError, ValidationError
from saltapi.repository.block_repository import BlockRepository
from saltapi.repository.proposal_repository import ProposalRepository


class DataRepository:
    def __init__(self, connection: Connection) -> None:
        self.connection = connection
        self.proposal_repository = ProposalRepository(connection)
        self.block_repository = BlockRepository(connection)

    def _get_data_format_id(self, data_format: str) -> int:
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
        block_visit_ids: List[int],
        data_formats: List[str],
    ) -> None:
        """
        Create an observation data request.
        """
        try:
            proposal_code_id = self.proposal_repository.get_proposal_code_id(
                proposal_code
            )
        except NotFoundError:
            raise ValidationError(f"Couldn't find proposal code '{proposal_code}'")

        proposal_block_visit_ids = [
            bv["id"] for bv in self.proposal_repository.block_visits(proposal_code)
        ]
        for bv_id in block_visit_ids:
            if bv_id not in proposal_block_visit_ids:
                raise ValidationError(
                    f"There exists no block visit with id {bv_id} for proposal "
                    f"{proposal_code}."
                )

        insert_rows: List[Dict[str, Any]] = []
        for data_format in data_formats:
            if data_format == "All":
                data_format_id = self._get_data_format_id("all")
                for block_visit_id in block_visit_ids:
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
        # While mypy and the SQLAlchemy documentation seem to suggest that you should
        # pass *insert_rows rather than insert_rows, this gives an error.
        self.connection.execute(
            stmt,
            insert_rows,  # ignore: type
        )
