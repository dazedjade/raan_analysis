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
      self.model = RaanModel()
      self.view = RaanAnalysisView(self)
      self.view.set_on_fetch_launches_callback(self.fetch_launch_data)
      self.view.display_record(None)


   # Callbacks for our UI events

   def fetch_launch_data(self, count):
      fetcher = LaunchDataFetchService(count)
      fetcher.fetch(self.model)

   def selected_record_changed(self, record_id: str):
      # Fetch record from model
      # Inject the LaunchRecord object into UI to update itself
      pass

   def raan_value_confirmed(self, record_id: str, raan_value: float):
      # Set raan value for the specified record
      pass
