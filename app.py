# Import packages
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import numpy as np
import plotly.express as px
import dash_bootstrap_components as dbc

external_stylesheets = [dbc.themes.MINTY]
app = Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "GROUP A - DATA101 Final Project"


app.layout = dbc.Container([
    # Navigation Bar
    dbc.NavbarSimple([
        dbc.NavItem(dbc.NavLink("BACKGROUND", href="#")),
        dbc.NavItem(dbc.NavLink("VISUALIZATIONS", href="#"))
    ],
        brand="GROUP A - Final Project",
        brand_href="#",
        color="#fffae5"
    ),

    # Landing Page
    dbc.Row([
        html.Div(
            html.H1("Dengue Severity in the Philippines", style={
                'padding': '50px',
                'text-align': 'center',
                'text-shadow': '1px 1px 1px #FFFFFF',
            })
        )
    ]),

    # Visualizations
    dbc.Row([

    ])


], fluid=True)

if __name__ == "__main__":
    app.run(debug=True)
