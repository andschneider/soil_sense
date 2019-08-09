import dash
from dash.dependencies import Input, Output, State
import dash.exceptions

from components.plots import Plot
from data_manager import DataManager


def setup_callbacks(app):
    dm = DataManager()
    print(" +++ callbacks setup")

    @app.callback(Output("slider-value", "children"), [Input("input-rolling", "value")])
    def display_slider_value(slider_input):
        return f"Select number of minutes for the rolling average ({slider_input}):"

    @app.callback(
        Output("subplots-live", "figure"),
        [
            Input("sensor-table", "selected_rows"),
            Input("input-minutes", "value"),
            Input("input-rolling", "value"),
            Input("button-get-data", "n_clicks"),
        ],
    )
    def update_plot(selected, minutes, rolling, button_click):
        # TODO the state is a workaround for the dcc.loading issue in layout.py but is not optimal
        ctx = dash.callback_context
        # print(f"inputs: {ctx.inputs}")
        # print(f"trigger: {ctx.triggered}")

        # get sensor ids from selected row in table
        sensor_ids = [dm.sensor_ids[s_id] for s_id in selected]

        # create blank plot
        plot = Plot()

        # on page load default to 10 minutes
        if not minutes:
            dm.update_sensor_data(10, sensor_ids)
            add_data_to_plot(plot, rolling, sensor_ids)
            return plot.figure

        # run when the button is clicked
        if ctx.triggered[0]["prop_id"].split("-")[0] == "button":
            print("updating plot by click")
            dm.update_sensor_data(int(minutes), sensor_ids)
            add_data_to_plot(plot, rolling, sensor_ids)
            return plot.figure

        # don't run
        else:
            raise dash.exceptions.PreventUpdate
            # return existing_state

    def add_data_to_plot(plot, rolling, sensor_ids):
        """Loops through all sensor ids and adds the data to be plotted. Also calculates the rolling average."""
        # TODO set the time to PCT timezone
        for sensor in sensor_ids:
            sensor_data = dm.sensor_data[sensor]
            # create a rolling average
            data_rolled = sensor_data.rolling(int(rolling), on="date").mean()
            # add data to plot
            plot.add_data(sensor_data, data_rolled, sensor)
            plot.add_alert_level(sensor_data, dm.alert_levels[sensor], sensor)
