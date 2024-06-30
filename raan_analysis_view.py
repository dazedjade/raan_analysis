from tkinter import  *
from tkinter import ttk
from typing import Callable
from gui_strings import Strings

class RaanAnalysisView:

    _fetch_launches_callback: Callable
    _fetch_count: StringVar

    def __init__(self, parent) -> None:
        self.style = ttk.Style()
        self._content = ttk.Frame(parent)
        self._content.pack()
        self._content.pack_configure(fill="both", expand=True)

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

        self._fetch_count = StringVar()
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

        self._launch_name_label = Label(entry_frame, text=Strings.LAUNCH_NAME)
        self._launch_id_label = Label(entry_frame, text=Strings.LAUNCH_ID)
        self._latitude_label = Label(entry_frame, text=Strings.LATITUDE)
        self._longitude_label = Label(entry_frame, text=Strings.LONGITUDE)
        self._net_label = Label(entry_frame, text=Strings.NET)
        self._sunrise_label = Label(entry_frame, text=Strings.SUNRISE)
        self._sunlight_hours_label = Label(entry_frame, text=Strings.SUNLIGHT_HOURS)

        self._launch_name_label.grid(row=0, column=0, sticky="nsew", columnspan=2)
        self._launch_id_label.grid(row=1, column=0, sticky="nsew")
        self._latitude_label.grid(row=2, column=0, sticky="nsew")
        self._longitude_label.grid(row=3, column=0, sticky="nsew")
        self._net_label.grid(row=1, column=1, sticky="nsew")
        self._sunrise_label.grid(row=2, column=1, sticky="nsew")
        self._sunlight_hours_label.grid(row=3, column=1, sticky="nsew")

        record_browser = RecordBrowser(entry_frame, ["abc", "def", "ghi"], self._selected_item_changed)
        record_browser.grid(row=4, column=2)
        
        entry_frame.rowconfigure(0, weight=1)
        entry_frame.columnconfigure(0, weight=1)

        data_entry_tab.rowconfigure(1, weight=1)
        data_entry_tab.columnconfigure(0, weight=1)

        # Move the labels to use StringVar and then no need to have them as vars
        # Need to bounce item display to controller, controller then pass record obj into the view to display by updating stringvars
        # On save button, we can bounce the new RAAN value to controller to push into the database
        # also call refresh on completion of loading launch data



    def _selected_item_changed(self, item_to_display):
        print(f"Displaying {item_to_display}")

    def set_on_fetch_launches_callback(self, callback: Callable | None):
        self._fetch_launches_callback = callback


    # Callbacks
    def _fetch_launches_pressed(self):
        if self._fetch_launches_callback is not None:
            self._fetch_launches_callback(self._fetch_count.get())

    

class RecordBrowser(Frame):
    """
    Custom navigation widget to shift between records.
    Source for custom widget: https://stackoverflow.com/questions/30489308/creating-a-custom-widget-in-tkinter
    """

    def __init__(self, parent, items: list, display_item_callback: Callable):
        Frame.__init__(self, parent)

        self._items = items
        self._current_index = 0
        self._display_item_changed = display_item_callback

        self._prev_button = Button(self, text="Prev", command=self._previous_record)
        self._position_label = Label(self)
        self._next_button = Button(self, text="Next", command=self._next_record)
        self._update_navigation_text()

        self._prev_button.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)
        self._position_label.grid(row=0, column=1, sticky="nsew", padx=2, pady=2)
        self._next_button.grid(row=0, column=2, sticky="nsew", padx=2, pady=2)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        
    def item_count(self) -> int:
        if self._items is None:
            return 0
        
        return len(self._items)
    
    def _previous_record(self):
        """
        Invoke navigation to previous record if not already at 0th entry
        """
        if self._items is None or self._current_index == 0:
            return
        
        # Safe to decrease the index and invoke the display change
        self._current_index -= 1
        item_to_display = self._items[self._current_index]
        self._display_item_changed(item_to_display)
        self._update_navigation_text()

        # Invoke the call back and pass the item's ID
        
    def _next_record(self):
        """
        Invoke navigation to next record if not already at last entry
        """
        if self._items is None or self._current_index >= self.item_count() - 1:
            return
        
        self._current_index += 1
        item_to_display = self._items[self._current_index]
        self._display_item_changed(item_to_display)
        self._update_navigation_text()

    def _update_navigation_text(self):
        self._position_label.configure(text=f"{self._current_index + 1} of {self.item_count()}")



