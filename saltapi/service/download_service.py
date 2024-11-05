import pathlib

from saltapi.settings import get_settings
from saltapi.repository.download_repository import DownloadRepository

settings = get_settings()


class DownloadService:
    def __init__(self, download_repository: DownloadRepository):
        self.download_repository = download_repository

    @staticmethod
    def get_slit_mask_xml_path(proposal_code: str) -> pathlib.Path:
        return get_settings().proposals_dir / proposal_code / "Included"

    @staticmethod
    def get_slit_mask_plot_path(proposal_code: str) -> pathlib.Path:
        return get_settings().proposals_dir / proposal_code / "Included"
