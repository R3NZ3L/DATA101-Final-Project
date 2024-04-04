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
provinces = gpd.read_file("datasets/json/provinces.json")
regions_gdf = regions[["adm1_psgc", "geometry"]].merge(
    cdpr, on="adm1_psgc").set_index("adm1_psgc")

per_month = main_df[['region', 'month_num', 'month_name', 'cases', 'deaths']].groupby(
    ['region', 'month_num', 'month_name'])[['cases', 'deaths']].sum().reset_index()
national = per_month.groupby(["month_num", "month_name"])[
    ["cases", "deaths"]].sum().reset_index()
national["Region"] = "Philippines - National Aggregate"
dropdown_options = [{'label': 'All regions', 'value': 'all'}] + \
    [{'label': region, 'value': region}
        for region in per_month['region'].unique()]

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
                'padding': '125px',
                'text-align': 'center',
                'text-shadow': '2px 2px 2px black',
                'color': 'white',  # Text color
                # Background image
                'background-image': 'url("https://github.com/R3NZ3L/DATA101-Final-Project/blob/main/assets/header.png?raw=true")',
                'background-size': 'cover',  # Ensure the image covers the entire div
                'background-position': 'center',  # Center the image
                'height': '300px',  # Height of the div
            })
        )
    ]),

    html.Div([
        html.H4(
            ["There were ", html.Strong("91,000+"), " confirmed dengue infections and ", html.Strong(
                "1,100+"), " confirmed deaths from ", html.Strong("Dengue"), " in 2020 "],
            style={
                'padding': '25px',
                'text-align': 'center'
            }
        ),

        html.Br(),
        html.Br(),

        # Landing Page Text and Images
        dbc.Row([
                dbc.Col([
                    html.H5("Dengue is not Uncommon in the Philippines"),
                    html.P("Every year, tens and even hundreds of thousands of Filipinos contract this illness, and many succumb to it. The 2019 dengue outbreak was one of the worst years for the country, wherein it has reported the highest number of cases and deaths across Southeast Asia (Santos, 2019). The impact was severe, with over 370,000 cases, and 1400 casualties recorded in a single year (World Health Organization, 2019).", style={
                        'text-align': 'justify'})
                ], width=8),
                dbc.Col([
                    html.Img(
                        src="https://github.com/R3NZ3L/DATA101-Final-Project/blob/main/assets/hospital_picture1.jpg?raw=true", style={'width': '100%'}),
                ], width=4),
                ]),

        html.Br(),
        html.Br(),

        dbc.Row([
                dbc.Col([
                    html.Img(src="https://github.com/R3NZ3L/DATA101-Final-Project/blob/main/assets/hospital_picture2.png?raw=true",
                             style={'width': '100%'}),
                ], width=4),
                dbc.Col([
                    html.H5("The Vital Role of Accessible Healthcare"),
                    html.P("The World Health Organization (2022) emphasizes that timely medical care and early detection can reduce dengue fatality rates to less than 1%. Research by Lum et al. (2014) underscores the significance of basic primary care access in mitigating dengue-related morbidity and mortality. Freitas et al. (2019) further support this, revealing that inadequate healthcare access leads to delayed treatment, with 90% of dengue fatalities occurring due to late admission to medical facilities in areas with limited healthcare infrastructure.", style={
                        'text-align': 'justify'}),
                ], width=8),
                ]),
        html.Br(),
        html.Br(),

        dbc.Row([
                dbc.Col([
                    html.H5("Our goal for this Project:"),
                    html.P("Our project aims to shed light on the severity of Dengue in the regions and cities of the Philippines. Through visualizations - the use of graphs, charts, and maps, we will illustrate the incidence of dengue cases, deaths, and fatality rates across different cities, allowing for comparisons to identify the most and least affected areas. Additionally, we intend to identify notable regions with high and low dengue fatality rates to establish focal points for further investigation and intervention efforts.  By utilizing data visualization techniques, we aim to not only raise awareness about the pressing healthcare challenges faced by certain communities but also to inform targeted interventions aimed at mitigating the impact of dengue outbreaks in the Philippines.", style={
                        'text-align': 'justify'})
                ], width=8),
                dbc.Col([
                    html.Img(
                        src="https://github.com/R3NZ3L/DATA101-Final-Project/blob/main/assets/person_picture3.jpg?raw=true", style={'width': '100%'}),
                ], width=4),
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
        ]),

        html.Br(),
        html.Hr(),
        # Line Chart - Insert words here
        html.Div([
            dcc.Graph(
                figure={},
                id='bc_line'
            )
        ]),
        dbc.Row([
                dbc.Col([
                    dbc.Row([
                        dbc.Col([
                            html.H5("Line Depth:"),
                            dcc.RadioItems(
                                id='line_depth',
                                options=[
                                    {'label': 'Regional', 'value': 'region'},
                                    {'label': 'National', 'value': 'national'}
                                ],
                                value='region'  # Default value
                            )
                        ]),
                        dbc.Col([
                            html.H5("Variable:"),
                            dcc.RadioItems(
                                id='line_variable',
                                options=[
                                    {'label': 'Cases', 'value': 'cases'},
                                    {'label': 'Deaths', 'value': 'deaths'}
                                ],
                                value='cases'  # Default value
                            )
                        ]),
                        dbc.Col([
                            html.H5("Select Region:"),
                            dcc.Dropdown(
                                id='region_dropdown',
                                options=dropdown_options,
                                value='all',
                                style={'width': '500px'},  # Default value
                                clearable=False  # Disable option to clear selection
                            )
                        ])
                    ])
                ], width=10)
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


@callback(
    Output("bc_line", "figure"),
    [Input("line_depth", "value"),
     Input("line_variable", "value"),
     Input("region_dropdown", "value")]
)
def update_bc_line(line_depth, line_variable, region_dropdown):
    if line_depth == "region":
        if region_dropdown == 'all':
            fig = px.line(per_month,
                          x="month_name",
                          y=line_variable,
                          color="region",
                          labels={
                              'month_name': 'Month',
                              'cases': 'Number of Cases',
                              'deaths': 'Number of Deaths',
                              'region': 'Region'
                          }
                          )
        else:
            filtered_data = per_month[per_month['region'] == region_dropdown]
            fig = px.line(filtered_data,
                          x="month_name",
                          y=line_variable,
                          color="region",
                          labels={
                              'month_name': 'Month',
                              'cases': 'Number of Cases',
                              'deaths': 'Number of Deaths',
                              'region': 'Region'
                          }
                          )
    elif line_depth == "national":
        fig = px.line(national,
                      x="month_name",
                      y=line_variable,
                      color="Region",
                      labels={
                          'month_name': 'Month',
                          'cases': 'Number of Cases',
                          'deaths': 'Number of Deaths',
                          'Region': 'Region'
                      }
                      )

    return fig


if __name__ == "__main__":
    app.run(debug=True, port=8055)
