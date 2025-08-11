from dataclasses import dataclass
from aiassistentshowcase.agents.tools.database_connection import DatabaseConnection

@dataclass
class DBDependencies:
    db : DatabaseConnection
