import tkinter as tk
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

   def fetch_launch_data(self, count):
      fetcher = LaunchDataFetchService(count)
      fetcher.fetch(self.model)
