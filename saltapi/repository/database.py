from typing import Any

from sqlalchemy import create_engine

from saltapi.settings import get_settings

_engine: Any = None


def engine() -> Any:
    global _engine
    if not _engine:
        sdb_dsn = get_settings().sdb_dsn
        echo_sql = get_settings().echo_sql
        _engine = create_engine(sdb_dsn, echo=echo_sql, future=True)
    return _engine
