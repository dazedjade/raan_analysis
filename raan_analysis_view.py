import datetime
from tkinter import  *
from tkinter import ttk
from tkinter import messagebox
from typing import Callable
from gui_strings import Strings
from launch_record import LaunchRecord
from raan_entry import RaanEntry
from record_browser import RecordBrowser

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
    _csv_file_name: StringVar
    _pdf_file_name: StringVar

    def __init__(self, parent) -> None:
        
        self._initialise_string_vars()
        self._make_root_content(parent)
        self._make_tab_container(self._content)
        self._make_data_entry_tab(self._data_entry_tab)
        self._make_analysis_tab(self._data_analysis_tab)
        

    # View Construction
    # Note: This would benefit from self contained components similar to RecordBrowser and RaanEntry
    # However, because of time constraint, this view code will have to remain here. :(

    def _initialise_string_vars(self):
        self._fetch_count = StringVar()
        self._launch_name = StringVar()
        self._launch_id = StringVar()
        self._latitude = StringVar()
        self._longitude = StringVar()
        self._net_datetime = StringVar()
        self._sunrise_datetime = StringVar()
        self._sunlight_hours = StringVar()
        self._csv_file_name = StringVar()
        self._pdf_file_name = StringVar()

    def _make_root_content(self, parent: Tk):
        self.style = ttk.Style()
        self._content = ttk.Frame(parent)
        self._content.pack()
        self._content.pack_configure(fill="both", expand=True)

    def _make_tab_container(self, parent: Tk):
        self._tab_container = ttk.Notebook(parent)
        self._data_entry_tab = ttk.Frame(self._tab_container)
        self._data_analysis_tab = ttk.Frame(self._tab_container)
        self._tab_container.add(self._data_entry_tab, text=Strings.DATA_FETCH)
        self._tab_container.add(self._data_analysis_tab, text=Strings.ANALYSIS)
        self._tab_container.pack(expand=True, fill="both")

    def _make_data_entry_tab(self, parent: Tk):
        fetch_frame = LabelFrame(parent, text=Strings.LAUNCH_DATA_FETCHING)
        fetch_frame.grid(row=0, column=0, padx=5, pady=5, sticky="new")

        fetch_launches_label = Label(fetch_frame, text=Strings.FETCH_COUNT)
        fetch_launches_label.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        fetch_count_entry = Entry(fetch_frame, textvariable=self._fetch_count)
        fetch_count_entry.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        fetch_button = Button(fetch_frame, text=Strings.FETCH, command=self._fetch_launches_pressed)
        fetch_button.grid(row=0, column=2, sticky="nsew", padx=20, pady=20)

        entry_frame = LabelFrame(parent, text=Strings.DATA_ENTRY)
        entry_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        launch_name_label = Label(entry_frame, textvariable=self._launch_name)
        launch_id_label = Label(entry_frame, textvariable=self._launch_id)
        latitude_label = Label(entry_frame, textvariable=self._latitude)
        longitude_label = Label(entry_frame, textvariable=self._longitude)
        net_label = Label(entry_frame, textvariable=self._net_datetime)
        sunrise_label = Label(entry_frame, textvariable=self._sunrise_datetime)
        sunlight_hours_label = Label(entry_frame, textvariable=self._sunlight_hours)

        launch_name_label.grid(row=0, column=0, sticky="nsew", columnspan=2)
        launch_id_label.grid(row=1, column=0, sticky="nsw")
        latitude_label.grid(row=2, column=0, sticky="nsw")
        longitude_label.grid(row=3, column=0, sticky="nsw")
        net_label.grid(row=1, column=1, sticky="nsw")
        sunrise_label.grid(row=2, column=1, sticky="nsw")
        sunlight_hours_label.grid(row=3, column=1, sticky="nsw")

        self._raan_entry = RaanEntry(entry_frame, self._confirm_raan_entry)
        self._raan_entry.grid(row=4, column=0)

        self._record_browser = RecordBrowser(entry_frame, [], self._selected_item_changed)
        self._record_browser.grid(row=4, column=1)

        fetch_frame.rowconfigure(0, weight=1)
        fetch_frame.columnconfigure(0, weight=3)
        fetch_frame.columnconfigure(1, weight=1)
        fetch_frame.columnconfigure(2, weight=1)

        entry_frame.rowconfigure(0, weight=1)
        entry_frame.rowconfigure(4, weight=1)
        entry_frame.columnconfigure(0, weight=1)

        parent.rowconfigure(1, weight=1)
        parent.columnconfigure(0, weight=1)

    def _make_analysis_tab(self, parent: Tk):
        show_graph_button = Button(parent, text=Strings.SHOW_GRAPH, command=self._show_raan_sunlight_graph)
        csv_file_name_label = Label(parent, text=Strings.CSV_EXPORT_FILE_NAME)
        csv_file_name_entry = Entry(parent, textvariable=self._csv_file_name)
        export_csv_button = Button(parent, text=Strings.EXPORT_CSV, command=self._export_csv)
        pdf_file_name_label = Label(parent, text=Strings.PDF_EXPORT_FILE_NAME)
        pdf_file_name_entry = Entry(parent, textvariable=self._pdf_file_name)
        export_pdf_button = Button(parent, text=Strings.EXPORT_PDF, command=self._export_pdf)

        show_graph_button.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        csv_file_name_label.grid(row=0, column=1, padx=5, pady=5, sticky="nse")
        csv_file_name_entry.grid(row=0, column=2, padx=5, pady=5, sticky="nsew")
        export_csv_button.grid(row=0, column=3, padx=5, pady=5, sticky="nsew")
        pdf_file_name_label.grid(row=0, column=4, padx=5, pady=5, sticky="nse")
        pdf_file_name_entry.grid(row=0, column=5, padx=5, pady=5, sticky="nsew")
        export_pdf_button.grid(row=0, column=6, padx=5, pady=5, sticky="nsew")

        parent.columnconfigure(0, weight=1)
        parent.columnconfigure(1, weight=1)
        parent.columnconfigure(3, weight=1)
        parent.columnconfigure(4, weight=1)
        parent.columnconfigure(6, weight=1)


    # Public methods to update view state

    def display_record(self, launch_record: LaunchRecord):
        """
        Update view with data from the passed record

        Args:
        launch_record: Contains data to display on view
        """
        if launch_record is None:
            # When a null record is passed, use a default display
            launch_record = LaunchRecord.empty_record()

        self._launch_name.set(f"{Strings.LAUNCH_NAME}: {launch_record.name}")
        self._launch_id.set(f"{Strings.LAUNCH_ID}: {launch_record.launch_id}")
        self._latitude.set(f"{Strings.LATITUDE}: {launch_record.latitude}")
        self._longitude.set(f"{Strings.LONGITUDE}: {launch_record.longitude}")
        self._net_datetime.set(f"{Strings.NET}: {datetime.datetime.fromtimestamp(launch_record.net)}")
        self._sunrise_datetime.set(\
            f"{Strings.SUNRISE}: {datetime.datetime.fromtimestamp(launch_record.sunrise_timestamp)}")
        self._sunlight_hours.set(f"{Strings.SUNLIGHT_HOURS}: {launch_record.hours_of_sunlight:.{3}}")
        self._raan_entry.display_existing_raan_value(launch_record.raan)

    def display_items_list(self, items: list):
        self._record_browser.set_items(items)

    
    # Setters for callback connecting

    def set_on_fetch_launches_callback(self, callback: Callable | None):
        self._fetch_launches_callback = callback

    def set_selected_record_changed_callback(self, callback: Callable | None):
        self._selected_record_changed_callback = callback

    def set_confirm_raan_entry_callback(self, callback: Callable | None):
        self._confirm_raan_entry_callback = callback

    def set_show_graph_callback(self, callback: Callable | None):
        self._show_graph_callback = callback

    def set_export_data_to_csv_callback(self, callback: Callable | None):
        self._export_csv_callback = callback

    def set_export_graph_to_pdf_callback(self, callback: Callable | None):
        self._export_pdf_callback = callback

    
    # Callbacks for UI events that we're going to bounce up to the view controller

    def _fetch_launches_pressed(self):
        if self._fetch_launches_callback is not None:
            self._fetch_launches_callback(self._fetch_count.get())

    def _selected_item_changed(self, item_to_display: str):
        if self._selected_record_changed_callback is not None:
            self._selected_record_changed_callback(item_to_display)

    def _confirm_raan_entry(self, raan_value: float):
        if self._confirm_raan_entry_callback is not None:
            record_id = self._record_browser.selected_item()
            self._confirm_raan_entry_callback(record_id, raan_value)

    def _show_raan_sunlight_graph(self):
        if self._show_graph_callback is not None:
            self._show_graph_callback()

    def _export_csv(self):
        # Using basic checks for file name extension due to time constraints.
        file_name = self._csv_file_name.get()
        if file_name is None or file_name == "":
            messagebox.showinfo(message="Please enter a name for the csv file")
            return
        
        if file_name.find(".csv") == -1:
            file_name += ".csv"
        
        if self._export_csv_callback is not None:
            self._export_csv_callback(file_name)

    def _export_pdf(self):
        file_name = self._pdf_file_name.get()
        if file_name is None or file_name == "":
            messagebox.showinfo(message="Please enter a name for the pdf file")
            return
        
        if file_name.find(".pdf") == -1:
            file_name += ".pdf"

        if self._export_pdf_callback is not None:
            self._export_pdf_callback(file_name)
