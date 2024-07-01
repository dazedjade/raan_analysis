import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from launch_data_fetch_service import LaunchDataFetchService
from raan_analysis_model import RaanModel
from raan_analysis_view import RaanAnalysisView
from pandas import DataFrame
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

   def _show_raan_sunlight_graph(self, use_total_hours: bool):
      """
      Draw a scatter graph to screen showing correlation between RAAN and
      total hours of sunlight on launch day or hours of sunlight before launch,
      depending on passed args.

      Args:
      use_total_hours: If true, graph will use total sunlight hours on launch day, otherwise
                        it will use the hrs of sunlight before launch.
      """
      self._plot_graph(use_total_hours)
      plt.show()


   def _export_data_to_csv(self, file_name: str, use_total_hours: bool):
      """
      Export data to csv. Conent of data depends on passed args.

      Args:
      file_name: Name of the file to export csv to.
      use_total_hours: If true, graph will use total sunlight hours on launch day, otherwise
                        it will use the hrs of sunlight before launch.
      """
      df: DataFrame = None
      if use_total_hours:
         df = self._model.as_pandas_frame_total_sunlight()
      else:
         df = self._model.as_pandas_frame_hours_before_net()
      df.to_csv(file_name)
      messagebox.showinfo(message=f"Exported data to {file_name}")

   def _export_graph_to_pdf(self, file_name: str, use_total_hours: bool):
      """
      Plot graph based and export to pdf. Graph content depends on passed args

      Args:
      file_name: Name of the file to export pdf to.
      use_total_hours: If true, graph will use total sunlight hours on launch day, otherwise
                        it will use the hrs of sunlight before launch.
      """
      self._plot_graph(use_total_hours)
      plt.savefig(file_name)
      messagebox.showinfo(message=f"Exported graph to {file_name}")

   def _plot_graph(self, use_total_hours: bool):
      """
      Plots graph for either total daylight on launch day or hrs. sunlight before launch
      Graph can either be dispayed on screen or exported to pdf.

      Args:
      use_total_hours: If true, graph will use total sunlight hours on launch day, otherwise
                        it will use the hrs of sunlight before launch.
      """
      df: DataFrame = None
      graph_title: str = None
      y_axis_label: str = None
      y_axis_field_name: str = None
      
      if use_total_hours:
         df = self._model.as_pandas_frame_total_sunlight()
         graph_title = "Correlation between RAAN and hours of sunlight on launch day."
         y_axis_label = "Hrs. Sunlight on Launch Day"
         y_axis_field_name = "hours_of_sunlight"
      else:
         df = self._model.as_pandas_frame_hours_before_net()
         graph_title = "Correlation between RAAN and hours of sunlight before launch NET."
         y_axis_label = "Hrs. Sunlight Before Launch NET"
         y_axis_field_name = "sunlight_hours_before_launch"

      df.plot(\
         title=graph_title, \
         kind="scatter", \
         grid=True, \
         x="raan", \
         xlabel="RAAN", \
         xlim=(0, 360), \
         y=y_axis_field_name, \
         ylabel=y_axis_label)


