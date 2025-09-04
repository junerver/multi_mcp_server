
from typing import TypedDict


class MysqlDatabaseConfig(TypedDict):
    host: str
    port: int
    user: str
    password: str
    database: str
