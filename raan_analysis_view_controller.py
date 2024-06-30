import tkinter as tk
from launch_data_fetch_service import LaunchDataFetchService
from raan_analysis_model import RaanModel
from raan_analysis_view import RaanAnalysisView
from tkinter import messagebox

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
      self._view.set_show_graph_callback(self._show_raan_sunlight_graph)
      self._view.set_export_data_to_csv_callback(self._export_data_to_csv)
      self._view.set_export_graph_to_pdf_callback(self._export_graph_to_pdf)


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
      success = self._model.upsert_raan_value(record_id, raan_value)
      if not success:
         messagebox.showinfo(message="Unable to write RAAN value to database. Check log for more information.")

   def _show_raan_sunlight_graph(self):
      pass

   def _export_data_to_csv(self, file_name: str):
      pass

   def _export_graph_to_pdf(self, file_name: str):
      pass
