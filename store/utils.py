# yourapp/utils.py
import mysql.connector
import pandas as pd
import plotly.express as px

def get_database_plot():
    connection = mysql.connector.connect(
        host="your_host",
        user="your_username", 
        password="your_password",
        database="your_database"
    )

    query = "SELECT * FROM your_table"
    df = pd.read_sql(query, connection)

    fig = px.line(df, x='date_column', y='value_column')
    return fig.to_html(full_html=False)