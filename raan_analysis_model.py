import sqlite3
from typing import Final

class RaanModel:

    _DB_NAME: Final[str] = "past_launches.sqlite3"

    def __init__(self) -> None:
        self._initialise_database()

    def __del__(self):
        self.cursor.close()
        self.db_connection.close()

    # We're using SQLite, so fetch the database or create if it doesn't exist
    def _initialise_database(self):
        self.db_connection = sqlite3.connect(self._DB_NAME)
        self.cursor = self.db_connection.cursor()
        try:
            self.cursor.execute(
                """CREATE TABLE IF NOT EXISTS launch (
                id TEXT PRIMARY KEY,
                name TEXT,
                latitude TEXT,
                longitude TEXT,
                net_precision INTEGER,
                success INTEGER
                )"""
            )
        except sqlite3.DatabaseError as error:
            print("Error creating table:\n" + error)
