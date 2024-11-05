from sqlalchemy.engine import Connection


class DownloadRepository:
    def __init__(self, connection: Connection) -> None:
        self.connection = connection