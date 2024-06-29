import tkinter as tk
import raan_analysis_model as raan_model
import raan_analysis_view as raan_view

# By having our view controller extend Tkinter, we can encapsulate all
# behaviour and make use of a Model View Controller pattern.
class RaanAnalysisViewController(tk.Tk):

   def __init__(self) -> None:
      super().__init__()

      self.title("RAAN Daylight Analysis Tool")
      # self.model = raan_model.RaanModel()
      self.view = raan_view.RaanAnalysisView(self)
      self.view.set_on_fetch_launches_callback(self.fetch_launch_data)

   def fetch_launch_data(self, count):
      print("Fetch " + count + " launches")
