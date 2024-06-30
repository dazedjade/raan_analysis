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
        raan_value_entry.grid(row=0, column=1, sticky="nsew")
        confirm_button.grid(row=0, column=2, sticky="nsew")

        self.columnconfigure(0, weight=3)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(0, weight=2)


    def _confirm_raan_pressed(self):
        self._raan_confirm_callback(self._raan_value.get())
