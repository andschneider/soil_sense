import dash_table

from data_manager import DataManager


def create_sensor_table():
    dm = DataManager()
    table = dash_table.DataTable(
        id="sensor-table",
        columns=[
            {"name": i.replace("_", " "), "id": i} for i in ["sensor_id", "plant_name"]
        ],
        data=dm.plant_names,
        is_focused=True,
        row_selectable="multi",
        selected_rows=[0],
        # sort_action="native",
        # sort_mode="multi",
        style_header={"backgroundColor": "white", "fontWeight": "bold"},
        style_cell={"textAlign": "center", "fontSize": 14, "font-family": "sans-serif"},
        # style_cell_conditional=[
        #     {"if": {"row_index": "odd"}, "backgroundColor": "rgb(248, 248, 248)"}
        # ],
        editable=False,
        style_as_list_view=True,
    )
    return table
