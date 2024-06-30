import tkinter as tk
from launch_record import LaunchRecord
from raan_analysis_model import RaanModel
from raan_analysis_view import RaanAnalysisView
from launch_data_fetch_service import LaunchDataFetchService

# By having our view controller extend Tkinter, we can encapsulate all
# behaviour and make use of a Model View Controller pattern.
class RaanAnalysisViewController(tk.Tk):

   def __init__(self) -> None:
      super().__init__()

      self.title("RAAN Daylight Analysis Tool")
      self._model = RaanModel()

      self._view = RaanAnalysisView(self)
      self._view.set_on_fetch_launches_callback(self._fetch_launch_data)
      self._view.set_selected_record_changed_callback(self._selected_record_changed)
      self._view.set_confirm_raan_entry_callback(self._raan_value_confirmed)
      self._view.display_record(None)
      self._view.display_items_list(self._model.query_all_record_ids())


   # Callbacks for our UI events

   def _fetch_launch_data(self, count):
      fetcher = LaunchDataFetchService(count)
      fetcher.fetch(self.model)

   def _selected_record_changed(self, record_id: str):
      # Fetch record from model
      # Inject the LaunchRecord object into UI to update itself
      launch_record = self._model.query_launch_record(record_id)
      self._view.display_record(launch_record)

   def _raan_value_confirmed(self, record_id: str, raan_value: float):
      self._model.upsert_raan_value(record_id, raan_value)
