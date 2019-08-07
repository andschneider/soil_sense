import dash_core_components as dcc
import dash_html_components as html

from components.reusable import Card, Column, Comment
from components.sensor_table import create_sensor_table


def get_layout():
    return html.Div(
        html.Div(
            [
                Column(
                    width=3,
                    children=[
                        Comment("**SOIL SENSE v0.3.0**"),
                        Card(
                            children=[
                                html.P("Select sensors to plot:"),
                                create_sensor_table(),
                            ]
                        ),
                        Card(
                            children=[
                                html.P("Select number of minutes of data to plot:"),
                                dcc.Input(id="input-minutes", placeholder="10"),
                                html.Div(style={"padding": "15px"}),
                                html.Div(id="slider-value"),
                                dcc.Slider(
                                    id="input-rolling",
                                    min=0,
                                    max=120,
                                    step=1,
                                    value=60,
                                    marks={
                                        i: str(i) for i in [1, 20, 40, 60, 80, 100, 120]
                                    },
                                ),
                                html.Div(style={"padding": "15px"}),
                                html.Div(style={"padding": "15px"}),
                                html.Button("Plot Data", id="button-get-data"),
                            ]
                        ),
                    ],
                ),
                Column(
                    width=9,
                    children=[
                        Card(
                            children=[
                                # TODO using the loading state is a nice feature but it's causing problems with the
                                # displaying the graph when the settings are changed but not plotted
                                # TODO look into this later
                                # dcc.Loading(
                                dcc.Graph(
                                    id="subplots-live",
                                    style=dict(width="100%", height="80vh"),
                                ),
                                # 'graph', 'cube', 'circle', 'dot', 'default'
                                # type="dot"
                                # )
                            ]
                        )
                    ],
                ),
            ]
        )
    )
