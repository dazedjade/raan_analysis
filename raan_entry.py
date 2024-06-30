from tkinter import  *
from typing import Callable
from gui_strings import Strings

class RaanEntry(Frame):
    """
    Custom entry widget for entering RAAN values
    """

    _raan_value: StringVar
    _raan_confirm_callback: Callable

    def __init__(self, parent, confirm_entry_callback: Callable, current_raan: float = 0):
        Frame.__init__(self, parent)

        self._raan_value = StringVar(value=current_raan)
        self._raan_confirm_callback = confirm_entry_callback

        raan_value_label = Label(self, text=Strings.RAAN_VALUE)
        raan_value_entry = Entry(self, textvariable=self._raan_value)
        confirm_button = Button(self, text=Strings.CONFIRM, command=self._confirm_raan_pressed)

        raan_value_label.grid(row=0, column=0, sticky="nsew")
        raan_value_entry.grid(row=0, column=1, sticky="nsw")
        confirm_button.grid(row=0, column=2, sticky="nsw")

        self.columnconfigure(0, weight=3)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(0, weight=2)

    def display_existing_raan_value(self, raan_value: float | None):
        if raan_value is None:
            self._raan_value.set("")
        else:
            self._raan_value.set(raan_value)

    def _confirm_raan_pressed(self):
        entered_raan_value = self._raan_value.get()
        set_to_value = ":NULL"
        try:
            raan_float = float(entered_raan_value)
            if raan_float >= 0 and raan_float <= 360:
                set_to_value = raan_float
            else:
                print("RAAN value not in bounds of 0 to 360, so setting to null.")
        except ValueError:
            print("Unable to parse enterd RAAN value, setting to null.")

        self._raan_confirm_callback(set_to_value)
