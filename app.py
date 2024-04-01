# Import packages
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import numpy as np
import plotly.express as px
import dash_bootstrap_components as dbc
import geopandas as gpd
import mapboxgl

mapboxgl.access_token = 'pk.eyJ1IjoicjNuejNsIiwiYSI6ImNsdTNlZ2w2ODB6MjIyanFodDR6NXl2MnMifQ.kveM31v-0p75V41iiEt3bQ'

external_stylesheets = [dbc.themes.MINTY]
app = Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "GROUP A - DATA101 Final Project"

# Loading datasets
main_df = pd.read_csv("datasets/csv/dengue_cleaned.csv")
cdpp = pd.read_csv("datasets/csv/cases_deaths_per_province.csv")
cdpr = pd.read_csv("datasets/csv/cases_deaths_per_region.csv")
regions = gpd.read_file("datasets/json/regions.json")
# provinces = gpd.read_file("datasets/json/provinces.json")
regions_gdf = regions[["adm1_psgc", "geometry"]].merge(cdpr, on="adm1_psgc").set_index("adm1_psgc")

# Discrete color scheme for Regional display
color_dict = {
    'BARMM': '#5B7FA4',
    'CAR': '#A27F5D',
    'MIMAROPA': '#00FF85',
    'NCR': '#585858',
    'Region I': '#2000FF',
    'Region II': '#DFFF00',
    'Region III': '#E100FF',
    'Region IV-A': '#1EFF00',
    'Region IX': '#FF0026',
    'Region V': '#00FFD9',
    'Region VI': '#FF9100',
    'Region VII': '#9A6595',
    'Region VIII': '#FF4CD5',
    'Region X': '#48B7AC',
    'Region XI': '#9D609F',
    'Region XII': '#629F60',
    'Region XIII': '#9FC13E'
}

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

    html.Div([
        # Landing Page Text and Images
        dbc.Row([

        ]),

        html.Hr(),

        # Visualizations
        dbc.Row([
            # Map
            dbc.Col([
                dcc.Graph(
                    figure={},
                    id='bc_map'
                )
            ], width=6),

            # Bar Chart
            dbc.Col([
                dbc.Row([
                    dcc.Graph(
                        figure={},
                        id='bc_bar'
                    )
                ]),
                # Controls
                dbc.Row([
                    dbc.Col([], width=6),
                    dbc.Col([
                        dbc.Row([
                            dbc.Col([
                                html.H5("Map Depth:"),
                                dcc.RadioItems(
                                    id='map_depth',
                                    options={
                                        'region': 'Regional',
                                        'province': 'Provincial'
                                    },
                                    value="region",
                                )
                            ]),
                            dbc.Col([
                                html.H5("Variable:"),
                                dcc.RadioItems(
                                    id='variable',
                                    options={
                                        'cases': 'Cases',
                                        'deaths': 'Deaths',
                                        'fatality_rate': 'Fatality Rate'
                                    },
                                    value="cases",
                                )
                            ])
                        ])
                    ], width=6)
                ])
            ], width=6)
        ])
    ],
        style={
            'padding': '50px 150px 50px 150px'
        }
    )


], fluid=True)


@callback(
    Output("bc_bar", "figure"),
    Input("map_depth", "value"),
    Input("variable", "value")
)
def update_bc_bar(map_depth, variable):
    if map_depth == "region":
        if variable == "cases":
            fig = px.bar(
                cdpr.sort_values(ascending=False, by="cases"),
                x="region", y="cases", color="cases",
                color_continuous_scale=px.colors.sequential.OrRd,
                labels={
                    "region": "Region",
                    "cases": "Number of Cases"
                },
                text_auto=True
            )
        elif variable == "deaths":
            fig = px.bar(
                cdpr.sort_values(ascending=False, by="deaths"),
                x="region", y="deaths", color="deaths",
                color_continuous_scale=px.colors.sequential.OrRd,
                labels={
                    "region": "Region",
                    "deaths": "Number of Deaths"
                },
                text_auto=True
            )
        elif variable == "fatality_rate":
            fig = px.bar(
                cdpr.sort_values(ascending=False, by="fatality_rate"),
                x="region", y="fatality_rate", color="fatality_rate",
                color_continuous_scale=px.colors.sequential.OrRd,
                labels={
                    "region": "Region",
                    "fatality_rate": "Fatality Rate (in %)"
                },
                text_auto=True
            )

    elif map_depth == "province":
        pass

    return fig.update_layout(margin=dict(t=10, b=50), height=400)


@callback(
    Output("bc_map", "figure"),
    Input("map_depth", "value"),
    Input("variable", "value")
)
def update_bc_map(map_depth, variable):
    if map_depth == "region":
        if variable == "cases":
            fig = px.choropleth_mapbox(
                regions_gdf,
                geojson=regions_gdf.geometry,
                locations=regions_gdf.index,
                color="cases",
                color_continuous_scale=px.colors.sequential.OrRd,
                center={"lat": 12.74, "lon": 120.9803},
                mapbox_style="open-street-map",
                zoom=4.335
            )

    elif map_depth == "province":
        pass

    return fig.update_layout(margin=dict(t=10, b=50), height=550)


if __name__ == "__main__":
    app.run(debug=True)
