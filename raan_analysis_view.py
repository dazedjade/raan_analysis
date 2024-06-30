from tkinter import  *
from tkinter import ttk
from typing import Callable
from gui_strings import Strings
from record_browser import RecordBrowser
from raan_entry import RaanEntry

class RaanAnalysisView:

    _fetch_launches_callback: Callable
    _fetch_count: StringVar
    _launch_name: StringVar
    _launch_id: StringVar
    _latitude: StringVar
    _longitude: StringVar
    _net_datetime: StringVar
    _sunrise_datetime: StringVar
    _sunlight_hours: StringVar

    def __init__(self, parent) -> None:
        self.style = ttk.Style()
        self._content = ttk.Frame(parent)
        self._content.pack()
        self._content.pack_configure(fill="both", expand=True)

        self._fetch_count = StringVar()
        self._launch_name = StringVar()
        self._launch_id = StringVar()
        self._latitude = StringVar()
        self._longitude = StringVar()
        self._net_datetime = StringVar()
        self._sunrise_datetime = StringVar()
        self._sunlight_hours = StringVar()

        self._tab_container = ttk.Notebook(self._content)
        data_entry_tab = ttk.Frame(self._tab_container)
        data_analysis_tab = ttk.Frame(self._tab_container)
        self._tab_container.add(data_entry_tab, text=Strings.DATA_FETCH)
        self._tab_container.add(data_analysis_tab, text=Strings.ANALYSIS)
        self._tab_container.pack(expand=True, fill="both")

        fetch_frame = LabelFrame(data_entry_tab, text=Strings.LAUNCH_DATA_FETCHING)
        fetch_frame.grid(row=0, column=0, padx=5, pady=5, sticky="new")

        fetch_launches_label = Label(fetch_frame, text=Strings.FETCH_COUNT)
        fetch_launches_label.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        fetch_count_entry = Entry(fetch_frame, textvariable=self._fetch_count)
        fetch_count_entry.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        self._fetch_button = Button(fetch_frame, text=Strings.FETCH, command=self._fetch_launches_pressed)
        self._fetch_button.grid(row=0, column=2, sticky="nsew", padx=20, pady=20)
        
        fetch_frame.rowconfigure(0, weight=1)
        fetch_frame.columnconfigure(0, weight=3)
        fetch_frame.columnconfigure(1, weight=1)
        fetch_frame.columnconfigure(2, weight=1)

        entry_frame = LabelFrame(data_entry_tab, text=Strings.DATA_ENTRY)
        entry_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        launch_name_label = Label(entry_frame, textvariable=self._launch_name)
        launch_id_label = Label(entry_frame, textvariable=self._launch_id)
        latitude_label = Label(entry_frame, textvariable=self._latitude)
        longitude_label = Label(entry_frame, textvariable=self._longitude)
        net_label = Label(entry_frame, textvariable=self._net_datetime)
        sunrise_label = Label(entry_frame, textvariable=self._sunrise_datetime)
        sunlight_hours_label = Label(entry_frame, textvariable=self._sunlight_hours)

        launch_name_label.grid(row=0, column=0, sticky="nsew", columnspan=2)
        launch_id_label.grid(row=1, column=0, sticky="nsew")
        latitude_label.grid(row=2, column=0, sticky="nsew")
        longitude_label.grid(row=3, column=0, sticky="nsew")
        net_label.grid(row=1, column=1, sticky="nsew")
        sunrise_label.grid(row=2, column=1, sticky="nsew")
        sunlight_hours_label.grid(row=3, column=1, sticky="nsew")

        raan_entry = RaanEntry(entry_frame, self._confirm_raan_entry)
        raan_entry.grid(row=4, column=0)

        record_browser = RecordBrowser(entry_frame, ["abc", "def", "ghi"], self._selected_item_changed)
        record_browser.grid(row=4, column=1)
        
        entry_frame.rowconfigure(0, weight=1)
        entry_frame.columnconfigure(0, weight=1)

        data_entry_tab.rowconfigure(1, weight=1)
        data_entry_tab.columnconfigure(0, weight=1)


    def set_on_fetch_launches_callback(self, callback: Callable | None):
        self._fetch_launches_callback = callback

    def display_record(self, launch_record):
        """
        Update view with data from the passed record

        Args:
        launch_record: Contains data to display on view
        """

        self._launch_name.set(f"{Strings.LAUNCH_NAME}: ")
        self._launch_id.set(f"{Strings.LAUNCH_ID}: ")
        self._latitude.set(f"{Strings.LATITUDE}: ")
        self._longitude.set(f"{Strings.LONGITUDE}: ")
        self._net_datetime.set(f"{Strings.NET}: ")
        self._sunrise_datetime.set(f"{Strings.SUNRISE}: ")
        self._sunlight_hours.set(f"{Strings.SUNLIGHT_HOURS}: ")


    # Callbacks
    def _fetch_launches_pressed(self):
        if self._fetch_launches_callback is not None:
            self._fetch_launches_callback(self._fetch_count.get())

    def _selected_item_changed(self, item_to_display):
        print(f"Displaying {item_to_display}")

    def _confirm_raan_entry(self, raan_value):
        print(f"Confirm RAAN value: {raan_value}")


    # Need to bounce item display to controller, controller then pass record obj into the view to display by updating stringvars
    # On save button, we can bounce the new RAAN value to controller to push into the database
    # also call refresh on completion of loading launch data
