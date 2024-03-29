from typing import List

from saltapi.repository.data_repository import DataRepository


class DataService:
    def __init__(self, repository: DataRepository):
        self.repository = repository

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
        self.repository.request_data(
            user_id=user_id,
            proposal_code=proposal_code,
            block_visit_ids=block_visit_ids,
            data_formats=data_formats,
        )
