import sqlite3
from typing import Final

class RaanModel:

    _DB_NAME: Final[str] = "past_launches.db"

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
                    latitude TEXT NOT NULL,
                    longitude TEXT NOT NULL,
                    net INTEGER NOT NULL,
                    sunrise_timestamp INTEGER NOT NULL,
                    hours_of_sunlight INTEGER NOT NULL,
                    raan REAL
                );"""
            )
        except sqlite3.DatabaseError as error:
            print("Error creating table:\n" + error)

    def upsert_launch_record(self, \
            launch_id: str, \
            name: str, \
            latitude: str, \
            longitude: str, \
            net: int, \
            sunrise_timestamp: int, \
            hours_of_sunlight: int):
        
        try:
            # We set raan to null on creation, as user will enter via UI
            self.cursor.execute(f"""
                INSERT or REPLACE INTO launch VALUES (
                    "{launch_id}",
                    "{name}",
                    "{latitude}",
                    "{longitude}",
                    {net},
                    {sunrise_timestamp},
                    {hours_of_sunlight},
                    :NULL
                );
                """, \
                { 'NULL': None })
            self.db_connection.commit()
        except sqlite3.DatabaseError as error:
            print(f"Error iinserting record {id}:\n{error}")

