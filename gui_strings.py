from typing import Final

class Strings:

    DATA_FETCH: Final[str] = "Data Fetch/Entry"
    ANALYSIS: Final[str] = "Analysis"
    LAUNCH_DATA_FETCHING: Final[str] = "Lauch Data Fetching"
    FETCH_COUNT: Final[str] = "Number of launches to fetch:"
    FETCH: Final[str] = "Fetch!"
    DATA_ENTRY: Final[str] = "Data Entry"
    LAUNCH_NAME: Final[str] = "Launch name"
    LAUNCH_ID: Final[str] = "Launch ID"
    LATITUDE: Final[str] = "Latitude"
    LONGITUDE: Final[str] = "Longitude"
    NET: Final[str] = "Net"
    SUNRISE: Final[str] = "Sunrise"
    SUNLIGHT_HOURS: Final[str] = "Sunlight Hours"
    RAAN_VALUE: Final[str] = "RAAN Value:"
    CONFIRM: Final[str] = "Confirm"
    SHOW_GRAPH: Final[str] = "Show RAAN/Daylight Graph"
    CSV_EXPORT_FILE_NAME: Final[str] = "CSV export file name:"
    EXPORT_CSV: Final[str] = "Export CSV"
    PDF_EXPORT_FILE_NAME: Final[str] = "PDF export file name:"
    EXPORT_PDF: Final[str] = "Export PDF"
    SUNLIGHT_HOURS_MODE: Final[str] = \
        """
        If checked, graph and exports will use total sunlight hours for the launch day.
        If unchecked, the hours before launch net will be used and will result in negative
        values for hours of sunlight in cases where launch was before dawn.
        """
    ENTER_FILE_NAME_CSV: Final[str] = "Please enter a name for the csv file"
    ENTER_FILE_NAME_PDF: Final[str] = "Please enter a name for the pdf file"
    RAAN_OUT_OF_BOUNDS: Final[str] = "RAAN value not in bounds of 0 to 360, so setting to null."
    RAAN_PARSE_FAIL: Final[str] = "Unable to parse enterd RAAN value, likely by removing value, so setting to null."
