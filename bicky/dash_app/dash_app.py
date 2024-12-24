import dash
from dash import dcc, html
from dash.dependencies import Input, Output

# สร้าง Dash App
dash_app = dash.Dash(
    __name__,
    suppress_callback_exceptions=True,
    routes_pathname_prefix='/dash/',
)

# Layout ของ Dash
dash_app.layout = html.Div([
    html.H1("Hello from Dash!"),
    dcc.Input(id='input-text', type='text', placeholder='Enter something...'),
    html.Div(id='output-text'),
])

# Callback สำหรับ Dash
@dash_app.callback(
    Output('output-text', 'children'),
    [Input('input-text', 'value')]
)
def update_output(value):
    if not value:
        return "Please type something!"
    return f"You entered: {value}"
