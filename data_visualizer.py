import matplotlib.pyplot as plt
from pandas import DataFrame
from raan_analysis_model import RaanModel

class DataVisualizer:
    """
    Provides methods of visualising data, either in a graph onscreen, or exporting data to pdf/csv
    """

    def show_raan_sunlight_graph(self, model: RaanModel, use_total_hours: bool):
        """
        Draw a scatter graph to screen showing correlation between RAAN and
        total hours of sunlight on launch day or hours of sunlight before launch,
        depending on passed args.

        Args:
        use_total_hours: If true, graph will use total sunlight hours on launch day, otherwise
                            it will use the hrs of sunlight before launch.
        """
        self._plot_graph(model, use_total_hours)
        plt.show()

    def export_data_to_csv(self, model: RaanModel, file_name: str, use_total_hours: bool):
        """
        Export data to csv. Conent of data depends on passed args.

        Args:
        file_name: Name of the file to export csv to.
        use_total_hours: If true, graph will use total sunlight hours on launch day, otherwise
                            it will use the hrs of sunlight before launch.
        """
        df: DataFrame = None
        if use_total_hours:
            df = model.as_pandas_frame_total_sunlight()
        else:
            df = model.as_pandas_frame_hours_before_net()
        df.to_csv(file_name)

    def export_graph_to_pdf(self, model: RaanModel, file_name: str, use_total_hours: bool):
        """
        Plot graph based and export to pdf. Graph content depends on passed args

        Args:
        file_name: Name of the file to export pdf to.
        use_total_hours: If true, graph will use total sunlight hours on launch day, otherwise
                            it will use the hrs of sunlight before launch.
        """
        self._plot_graph(model, use_total_hours)
        plt.savefig(file_name)

    def _plot_graph(self, model: RaanModel, use_total_hours: bool):
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
            df = model.as_pandas_frame_total_sunlight()
            graph_title = "Correlation between RAAN and hours of sunlight on launch day."
            y_axis_label = "Hrs. Sunlight on Launch Day"
            y_axis_field_name = "hours_of_sunlight"
        else:
            df = model.as_pandas_frame_hours_before_net()
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
    