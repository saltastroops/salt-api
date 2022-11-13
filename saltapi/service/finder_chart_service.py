from pathlib import Path
from typing import Tuple

from saltapi.exceptions import NotFoundError
from saltapi.repository.finder_chart_repository import FinderChartRepository
from saltapi.settings import get_settings


class FinderChartService:
    def __init__(self, finder_chart_repository: FinderChartRepository):
        self.finder_chart_repository = finder_chart_repository

    def get_finder_chart(self, finder_chart_file: str) -> Tuple[str, Path]:
        """
        Return the proposal code and path of a finder chart.
        """
        proposals_directory = get_settings().proposals_dir
        path = Path(finder_chart_file)

        # Get the finder chart id, the filename prefix (if any) denoting the size and
        # the filename suffix
        name_parts = path.stem.split("-", maxsplit=1)
        finder_chart_id = int(name_parts[0])
        prefix = ""
        if len(name_parts) > 1:
            if name_parts[1] == "thumbnail":
                prefix = "Thumbnail"
            else:
                raise NotFoundError()

        suffix = path.suffix

        # The database stores a file path of a file which may have a suffix other than
        # the requested one. Hence we have to replace that suffix.
        proposal_code, finder_chart_path = self.finder_chart_repository.get(
            finder_chart_id
        )
        parent_dirs = str(finder_chart_path).split("/")[:-1]
        full_finder_chart_path = proposals_directory / proposal_code
        for d in parent_dirs:
            full_finder_chart_path /= d
        full_finder_chart_path /= f"{prefix}{finder_chart_path.stem}{suffix}"
        return proposal_code, Path(full_finder_chart_path).resolve()
