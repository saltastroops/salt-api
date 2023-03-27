from typing import List

from saltapi.repository.data_repository import DataRepository


class DataService:
    def __init__(self, repository: DataRepository):
        self.repository = repository

    def request_observations(
        self,
        user_id: int,
        proposal_code: str,
        block_visits_ids: List[int],
        data_formats: List[str],
    ):
        """
        Create an observations data request.
        """
        self.repository.request_observations(
            user_id=user_id,
            proposal_code=proposal_code,
            block_visits_ids=block_visits_ids,
            data_formats=data_formats,
        )
