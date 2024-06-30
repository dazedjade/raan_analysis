from tkinter import  *
from typing import Callable

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

    def set_items(self, items: list):
        """
        Assign the items that we want to browse through

        Args:
        items: List of items to navigate through

        Note:
        When setting a new set of items, the index is reset to 0 and the
        `_display_item_changed` event is invoked to keep the UI in sync.
        """
        self._items = items
        self._current_index = 0
        item_to_display = self._items[self._current_index]
        self._display_item_changed(item_to_display)
        self._update_navigation_text()
        
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
        item_count = self.item_count()
        selected_index =  self._current_index + 1 if item_count > 0 else 0
        self._position_label.configure(text=f"{selected_index} of {item_count}")