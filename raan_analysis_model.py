import pandas as pd
import sqlite3
from launch_record import LaunchRecord
from pandas import DataFrame
from typing import Final

class RaanModel:

    _DB_NAME: Final[str] = "past_launches.db"

    def __init__(self) -> None:
        self._initialise_database()

    def __del__(self):
        self._cursor.close()
        self._db_connection.close()

    # We're using SQLite, so fetch the database or create if it doesn't exist
    def _initialise_database(self):
        self._db_connection = sqlite3.connect(self._DB_NAME)
        self._cursor = self._db_connection.cursor()
        try:
            self._cursor.execute(
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
            self._cursor.execute(f"""
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
            self._db_connection.commit()
        except sqlite3.DatabaseError as error:
            print(f"Error inserting record {id}:\n{error}")

    def upsert_raan_value(self, launch_id: str, raan_value: float) -> bool:
        """
        Updates (or first write) RAAN value for the passed launch id.

        Args:
        launch_id: ID of the launch to set the RAAN for.
        raan_value: Value of RAAN to add to record.
        """
        try:
            self._cursor.execute(f"UPDATE launch SET raan={raan_value} WHERE id='{launch_id}'",  { 'NULL': None })
            self._db_connection.commit()
        except sqlite3.DatabaseError as error:
            print(f"Error writing RAAN value to record {launch_id}:\n{error}")
            return False
        
        return True

    def query_all_record_ids(self) -> list:
        """
        Returns a list of all contained launch record ids
        """
        try:
            self._cursor.execute(f"SELECT id FROM launch")
            results = self._cursor.fetchall()

            def extract_id(element):
                return element[0]

            # Result is contained in a tuple, so extract to a simple list of ids.
            launch_ids = list(map(extract_id, results))

            return launch_ids
        except sqlite3.DatabaseError as error:
            print(f"Error fetching record ids {error}")
            return []

    def query_launch_record(self, launch_id) -> LaunchRecord:
        """
        Get LaunchRecord instance for record with specified launch id

        Args:
        launch_id: String containg the id of the launch to fetch data for.

        Returns:
        LaunchRecord instance containing the launche's data or empty record if not found.
        """

        self._cursor.execute(f"SELECT * FROM launch WHERE id='{launch_id}'")
        record = self._cursor.fetchone()
        
        if record is None:
            print("Launch record not found, using default data")
            return LaunchRecord.empty_record()
        
        # Using named args here as record[n] isn't very clear
        return LaunchRecord(\
            launch_id=record[0], \
            name=record[1], \
            latitude=record[2], \
            longitude=record[3], \
            net=record[4], \
            sunrise_timestamp=record[5], \
            hours_of_sunlight=record[6], \
            raan=record[7])
    
    def as_pandas_frame_total_sunlight(self) -> DataFrame | None:
        """
        Loads database into a Pandas frame

        Returns: Pandas frame object containing launch records.
        """

        try:
            return pd.read_sql_query("SELECT hours_of_sunlight, raan FROM launch", self._db_connection)
        except sqlite3.DatabaseError as error:
            print(f"Error when reading db for pandas:\n{error}")
            return None
        
    def as_pandas_frame_hours_before_net(self) -> DataFrame | None:
        """
        Loads database into a Pandas frame with data needed to calculate hours of 
        sunlight before a launch.

        Returns: Pandas frame object containing launch records.
        """

        try:
            return pd.read_sql_query("""
            SELECT 
                raan,
                IIF(
                    ((net - sunrise_timestamp) / 3600.0) < hours_of_sunlight, 
                        ((net - sunrise_timestamp) / 3600.0), 
                        hours_of_sunlight
                    )
                AS sunlight_hours_before_launch
            FROM launch
            """, \
            self._db_connection)
        except sqlite3.DatabaseError as error:
            print(f"Error when reading db for pandas:\n{error}")
            return None
        
