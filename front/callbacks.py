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

        sensor_ids = [dm.sensor_ids[s_id] for s_id in selected]

        # create blank plot
        plot = Plot()

        # on page load default to 10 minutes
        if not minutes:
            dm.update_sensor_data(10, sensor_ids)
            for sensor in sensor_ids:
                data_rolled = (
                    dm.sensor_data[sensor].rolling(int(rolling), on="date").mean()
                )
                plot.add_data(dm.sensor_data[sensor], data_rolled, sensor)

            return plot.figure

        # run when the button is clicked
        if ctx.triggered[0]["prop_id"].split("-")[0] == "button":
            print("updating plot")
            dm.update_sensor_data(int(minutes), sensor_ids)

            # create a rolling average
            # TODO set the time to PCT timezone
            for sensor in sensor_ids:
                data_rolled = (
                    dm.sensor_data[sensor].rolling(int(rolling), on="date").mean()
                )
                plot.add_data(dm.sensor_data[sensor], data_rolled, sensor)

            return plot.figure

        # don't run
        else:
            raise dash.exceptions.PreventUpdate
            # return existing_state
