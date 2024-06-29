from tkinter import  *
from tkinter import ttk
from typing import Callable

class RaanAnalysisView:

    _fetch_launches_callback: Callable
    _fetch_count: StringVar

    def __init__(self, parent) -> None:
        # self.style = ttk.Style()
        self.content = ttk.Frame(parent)
        self.content.pack()
        self.content.pack_configure(fill="both", expand=True)

        fetch_frame = LabelFrame(self.content, text="Lauch Data Fetching")
        fetch_frame.pack()
        fetch_frame.pack_configure(padx=5,pady=5, anchor="n", fill="x", expand=True)

        fetch_launches_label = Label(fetch_frame, text="Number of launches to fetch:")
        fetch_launches_label.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        self._fetch_count = StringVar()
        fetch_count_entry = Entry(fetch_frame, textvariable=self._fetch_count)
        fetch_count_entry.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        self._fetch_button = Button(fetch_frame, text="Fetch!", command=self._fetch_launches_pressed)
        self._fetch_button.grid(row=0, column=2, sticky="nsew", padx=20, pady=20)
        
        fetch_frame.rowconfigure(0, weight=1)
        fetch_frame.columnconfigure(0, weight=3)
        fetch_frame.columnconfigure(1, weight=1)
        fetch_frame.columnconfigure(2, weight=1)

    def set_on_fetch_launches_callback(self, callback: Callable | None):
        self._fetch_launches_callback = callback


    # Callbacks
    def _fetch_launches_pressed(self):
        if self._fetch_launches_callback is not None:
            self._fetch_launches_callback(self._fetch_count.get())
        



