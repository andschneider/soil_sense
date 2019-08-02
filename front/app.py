import dash

from callbacks import setup_callbacks
from layout import get_layout


app = dash.Dash(__name__)
app.title = "soil-sense"


app.layout = get_layout()
setup_callbacks(app)

if __name__ == "__main__":
    app.run_server(host="0.0.0.0", debug=True, port=8050)
    # app.run_server(debug=True)
