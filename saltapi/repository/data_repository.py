from typing import List, cast

from sqlalchemy import text
from sqlalchemy.engine import Connection

from saltapi.repository.block_repository import BlockRepository
from saltapi.repository.proposal_repository import ProposalRepository
from saltapi.exceptions import NotFoundError, ValidationError


class DataRepository:
    def __init__(
        self,
        connection: Connection,
        block_repository: BlockRepository,
    ) -> None:
        self.connection = connection
        self.proposal_repository = ProposalRepository(connection)
        self.block_repository = block_repository

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
        block_visits_ids: List[int],
        data_formats: List[str],
    ):
        """
        Create an observation data request.
        """
        try:
            proposal_code_id = self.proposal_repository.get_proposal_code_id(
                proposal_code
            )
            proposal_codes = self.block_repository.get_proposal_codes_for_block_visits(
                block_visits_ids
            )
        except Exception:
            raise ValidationError()
        if block_visits_ids and not proposal_codes:
            #  As this method checks permissions, in principle there should be no
            #  validation. However, not ruling out observation ids of other proposals
            #  would constitute a security loophole, and hence we should ensure there are
            #  no such observation ids.
            raise ValidationError(f"Can't request data for other proposals.")
        for pc in proposal_codes:
            if pc != proposal_code:
                raise ValidationError(
                    f"Some of the observation ids belong the the proposal {pc}."
                )

        insert_rows = []
        for data_format in data_formats:
            data_format_id = self._get_data_format_id("all")
            if data_format == "all":
                for block_visit_id in block_visits_ids:
                    insert_rows.append(
                        {
                            "proposal_code_id": proposal_code_id,
                            "block_visit_id": block_visit_id,
                            "user_id": user_id,
                            "data_format_id": data_format_id,
                        }
                    )
            elif data_format == "calibration":
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
