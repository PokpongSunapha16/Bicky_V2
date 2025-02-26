import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px

def create_dash_app(server):
    # โหลดข้อมูล
    df = pd.read_csv('data/Electric_Vehicle_Population_Data.csv')
    ev_counts = df['Electric Vehicle Type'].value_counts().reset_index()
    ev_counts.columns = ['Electric Vehicle Type', 'Count']

    # สร้าง Dash App
    dash_app = dash.Dash(
        name='unique_dash_app',
        server=server,
        routes_pathname_prefix='/dash/'
    )

    # สร้าง Pie Chart
    fig = px.pie(
        ev_counts,
        names='Electric Vehicle Type',
        values='Count',
        title='Electric Vehicle Type Distribution'
    )

    # Layout
    dash_app.layout = html.Div([
        html.H1('Electric Vehicle Dashboard'),
        dcc.Graph(figure=fig)
    ])
