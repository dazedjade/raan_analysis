import os
import requests
from typing import Final

# Handles the fetch and parsing of data from API endpoint.
#
# Note: While we use the limit field in the launches/previous endpoint
# query, the data source uses it as a limit of the results per page.
# Therefore, we could make use of the result's "next" property to fetch
# another N number of records until we've consumed all available data.
class LaunchDataFetchService:

    # Define the URLs for each build environment
    # API_ENV is specified in launch.json
    _BASE_URL_ENVS: Final[dict] = {
        "DEV": "https://lldev.thespacedevs.com/",
        "PROD": "https://ll.thespacedevs.com/"
    }

    _compiled_url: str

    # Const strings
    _PREVIOUS_LAUNCHES_QUERY: Final[str] = "2.2.0/launch/previous/?limit=%s&search=Rocket Lab"
    _DB_NAME: Final[str] = "past_launches.sqlite3"
    _ENV_FIELD: Final[str] = "API_ENV"
    _ENV_PROD: Final[str] = "PROD"

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

    def fetch(self):
        try:
            results = requests.get(self._compiled_url)
        except Exception as error:
            print(f"Lanuch data error: {error}")
        else:
            status = results.status_code
            if status is 200:
                print(results.json())
