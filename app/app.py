import dash
from dash import dcc, html, Input, Output, State, callback_context
import dash_bootstrap_components as dbc
import pickle
import os

curdir = os.path.dirname(os.path.abspath(__file__))

model_path = os.path.join(curdir, '../notebooks/xgboost_model.pkl')
with open(model_path, 'rb') as f:
    model = pickle.load(f)

custom_styles = {
    'body': {
        'background-image': 'url("https://www.researchgate.net/profile/Li-Mingtao-2/publication/335483097/figure/fig3/AS:934217085100032@1599746118459/A-general-architecture-of-XGBoost.ppm")',
        'background-size': 'cover',
        'font-family': 'Arial, sans-serif',
    },
    'h1': {
        'color': 'blue',
        'background-color' : 'gray',
        'text-align': 'center',
        'margin-top': '50px',
    },
    'open-modal-button': {
        'display': 'flex',
        'background-color' : 'gray',
        'justify-content': 'center',
        'align-items': 'center', 
        'margin': '50px auto', 
        'max-width': '200px',  
    },
    'modal-content': {
        'background-color': '#ffffff',
        'border-radius': '10px',
        'position' : 'center',
    },
    'accuracy-output': {
        'background-color': '#e3f2fd',  
        'padding': '10px',
        'margin-top': '20px',
        'text-align': 'center',
        'border-radius': '5px',
    }
}


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

modal = dbc.Modal(
    [
        dbc.ModalHeader("Enter Your Information"),
        dbc.ModalBody(
            [
                html.Div(
                    [
                        html.Label("Weight (lbs)"),
                        dcc.Input(
                            id="weight",
                            type="number",
                            placeholder="Enter your weight",
                            debounce=True,
                            step=0.1,
                        ),
                    ],
                    className="mb-3",
                ),
                html.Div(
                    [
                        html.Label("Height (inches)"),
                        dcc.Input(
                            id="height",
                            type="number",
                            placeholder="Enter your height",
                            debounce=True,
                            step=0.1,
                        ),
                    ],
                    className="mb-3",
                ),
                html.Div(
                    [
                        html.Label("Age"),
                        dcc.Input(
                            id="age",
                            type="number",
                            placeholder="Enter your age",
                            debounce=True,
                            step=1,
                        ),
                    ],
                    className="mb-3",
                ),
                html.Div(
                    [
                        html.Label("Gender"),
                        dcc.Dropdown(
                            id="sex",
                            options=[
                                {"label": "Male", "value": "M"},
                                {"label": "Female", "value": "F"},
                            ],
                            placeholder="Select your gender",
                        ),
                    ],
                    className="mb-3",
                ),
            ]
        ),
        dbc.ModalFooter(
            [
                dbc.Button(
                    "Close", id="close-modal-button", className="btn-secondary"
                ),
                dbc.Button("Predict", id="predict-button", className="btn-primary"),
            ]
        ),
    ],
    id="modal",
    centered=True,
)

app.layout = html.Div(
    [
        html.H1("Treadmill Calories Accuracy Predictor", style=custom_styles['h1']),
        html.Div(
            html.Button("Open Modal", id="open-modal-button", className="btn-primary", style=custom_styles['open-modal-button']),
            style={'textAlign': 'center', 'marginTop': '50vh', 'transform': 'translateY(-50%)'},
        ),
        modal,
        html.Div(id="accuracy-output", style=custom_styles['accuracy-output']),
    ],
    style=custom_styles['body'],
)


@app.callback(
    Output("modal", "is_open"),
    [Input("open-modal-button", "n_clicks"), Input("close-modal-button", "n_clicks")],
    [State("modal", "is_open")],
)
def toggle_modal(open_clicks, close_clicks, is_open):
    ctx = callback_context
    if ctx.triggered_id in ["open-modal-button", "close-modal-button"]:
        return not is_open
    return is_open


@app.callback(
    Output("accuracy-output", "children"),
    [Input("predict-button", "n_clicks")],
    [
        State("weight", "value"),
        State("height", "value"),
        State("age", "value"),
        State("sex", "value"),
    ],
)
def predict_accuracy(n_clicks, weight, height, age, sex):
    if n_clicks:
        if not all([weight, height, age, sex]):
            return "Please fill out all fields"
        prediction = model.predict([[weight, height, age, 1 if sex == "M" else 0]])[0]
        return f"Predicted treadmill calories accuracy: {prediction:.2f}%"  


if __name__ == "__main__":
    app.run_server(debug=True)
