import plotly


class Plot:
    def __init__(self):
        self.figure = self._create_sub_plots()

    def add_data(self, data, rolled_data, sensor_id):
        """Creates traces and appends them to the figure."""
        temperature_trace, temperature_trace_rolled = self._create_traces(
            data, rolled_data, "temp", sensor_id
        )
        moist_trace, moist_trace_rolled = self._create_traces(
            data, rolled_data, "moisture", sensor_id
        )

        self.figure.append_trace(moist_trace, 1, 1)
        self.figure.append_trace(moist_trace_rolled, 1, 1)
        self.figure.append_trace(temperature_trace, 2, 1)
        self.figure.append_trace(temperature_trace_rolled, 2, 1)

    def add_alert_level(self, data, alert_level, sensor_id):
        """Add a horizontal line at an alert level."""
        trace = {
            "x": [data["date"][0], data["date"].iloc[-1]],
            "y": [alert_level, alert_level],
            "name": f"{sensor_id} alert",
            "mode": "lines",
            "type": "scatter",
            "line": dict(color="Red", width=1, dash="dash"),
        }
        self.figure.append_trace(trace, 1, 1)

    @staticmethod
    def _create_sub_plots():
        """Creates two blank plots, one for temperature and one for moisture sensor data. Actual data is added to plot later.

        Returns
        -------
        figure : Plotly figure
            A Plotly figure object to be passed to a Dash Graph object.

        """
        fig = plotly.tools.make_subplots(
            rows=2, cols=1, vertical_spacing=0.2, print_grid=False
        )
        fig["layout"]["margin"] = {"l": 50, "r": 10, "b": 50, "t": 10}
        fig["layout"]["legend"] = {
            # "x": 0.9,
            # "y": 0.47,
            "xanchor": "left",
            "bgcolor": "rgba(0,0,0,0)",
            # "bordercolor": "grey",
            # "borderwidth": 1,
            "orientation": "h",
        }

        # moisture traces
        fig["layout"]["xaxis1"].update(title="Date [UTC]")
        fig["layout"]["yaxis1"].update(title="Moisture [capacitance]")

        # temperature traces
        fig["layout"]["xaxis2"].update(title="Date [UTC]")
        fig["layout"]["yaxis2"].update(title="Temperature [F]")

        return fig

    @staticmethod
    def _create_traces(data, rolled_data, category, sensor_id):
        """Create a trace for raw and rolled data."""
        trace = {
            "x": data["date"],
            "y": data[category],
            "name": f"{sensor_id} {category} raw",
            "mode": "lines",
            "type": "scatter",
        }

        trace_rolled = {
            "x": rolled_data["date"],
            "y": rolled_data[category],
            "name": f"{sensor_id} {category} roll",
            "mode": "lines",
            "type": "scatter",
        }
        return trace, trace_rolled
