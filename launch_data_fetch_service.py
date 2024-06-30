import datetime
import json
import os
import requests
from typing import Final
from raan_analysis_model import RaanModel
from suntimes import SunTimes  

import test_json

# Handles the fetch and parsing of data from API endpoint.
#
# Note: While we use the limit field in the launches/previous endpoint
# query, the data source uses it as a limit of the results per page.
# Therefore, we could make use of the result's "next" property to fetch
# another N number of records until we've consumed all available data.
class LaunchDataFetchService:

    _compiled_url: str

    # Const strings
    _PREVIOUS_LAUNCHES_QUERY: Final[str] = "2.2.0/launch/previous/?limit=%s&search=Rocket Lab"
    _DB_NAME: Final[str] = "past_launches.sqlite3"
    _ENV_FIELD: Final[str] = "API_ENV"
    _ENV_PROD: Final[str] = "PROD"

    # Define the URLs for each build environment
    # API_ENV is specified in launch.json
    _BASE_URL_ENVS: Final[dict] = {
        "DEV": "https://lldev.thespacedevs.com/",
        "PROD": "https://ll.thespacedevs.com/"
    }

    # Construction of this object includes preparing the fetch query URL
    # Param:
    #   launches_count - the number of launches to fetch. If a negative or non-integer
    # is passed, this defaults to 0, and the endpoint will return a page of 10 results.
    def __init__(self, launches_count) -> None:

        # Default to PROD for cases where API_ENV isn't specified in os.environ
        base_url = self._BASE_URL_ENVS[self._ENV_PROD]
        if self._ENV_FIELD in os.environ:
            build_env = os.environ[self._ENV_FIELD]
            base_url = self._BASE_URL_ENVS[build_env]
        
        # Ensure the launch count request is a valid number
        limit = launches_count if launches_count.isdigit() else 0

        # Using string interpolation, we're able to build our fetch query URL
        self._compiled_url = base_url + self._PREVIOUS_LAUNCHES_QUERY %(limit)

    def fetch(self, model):
        try:
            results = requests.get(self._compiled_url)
        except Exception as error:
            print(f"Lanuch data error: {error}")
        else:
            status = results.status_code
            if status == 200:
                self._populate_database(data=results.json(), model=model)

        # To use test data without making API request, comment out the above and uncomment the below.
        # json_text = test_json.JSON_DATA
        # self._populate_database(data=json_text, model=model)

    def _populate_database(self, data, model: RaanModel):
        json_obj = json.JSONDecoder(strict=False).decode(data)

        # Using .get attempts to get the passed key (results) and returns
        # None if the specified key is not found within the object.
        launch_records = json_obj.get("results")
        if launch_records is None:
            return  # No records
        
        for record in launch_records:
            # Before parse/calculating other data, first attempt to fetch the data
            # that cannot be null - id, net, lat, lon
            launch_id = record.get("id")
            net = record.get("net")
            latitude = record.get("pad").get("latitude")
            longitude = record.get("pad").get("longitude")

            if launch_id is None or net is None or latitude is None or longitude is None:
                # Just log to console, but could propagte message in GUI
                # specifying that some records were skipped because of 
                # missing data. Could also check which property is missing.
                print("Got a record missing required data, so skipping.")
                continue

            launch_name = record.get("name")

            # We can calulate sunrise and hours of sun from lat/lon and net. Using UTC.
            lat_float = None
            lon_float = None
            try:
                lat_float = float(latitude)
                lon_float = float(longitude)
            except ValueError:
                print(f"Skipping record with invalid lat/lon values - {latitude}, {longitude}")
                continue

            net_datetime_format = "%Y-%m-%dT%H:%M:%SZ"
            launch_datetime = datetime.datetime.strptime(net, net_datetime_format)
            launch_day = datetime.datetime.combine(launch_datetime, datetime.time.min)

            sunlight_calculator = SunTimes(lon_float, lat_float)
            sunrise_time = sunlight_calculator.riseutc(launch_day).timestamp()
            sunset_time = sunlight_calculator.setutc(launch_day).timestamp()

            total_sunlight_hours = (sunset_time - sunrise_time) / 3600

            model.upsert_launch_record(\
                launch_id=launch_id, \
                name=launch_name, \
                latitude=latitude, \
                longitude=longitude, \
                net=launch_datetime.timestamp(), \
                sunrise_timestamp=sunrise_time, \
                hours_of_sunlight=total_sunlight_hours)
            





            


