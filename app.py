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

bc_region_dropdown_options = [
    'BARMM', 'CAR', 'MIMAROPA', 'NCR', 'Region I', 'Region II', 'Region III',
    'Region IV-A', 'Region IX', 'Region V', 'Region VI', 'Region VII', 'Region VIII',
    'Region X', 'Region XI', 'Region XII', 'Region XIII'
]

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
            html.H1("Philippine Dengue Severity Dashboard", style={
                'padding': '125px',
                'text-align': 'center',
                'text-shadow': '2px 2px 2px black',
                'color': 'white',
                'background-image': 'url("https://github.com/R3NZ3L/DATA101-Final-Project/blob/main/assets/header.png?raw=true")',
                'background-size': 'cover',
                'background-position': 'center',
                'height': '300px',
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
                    html.H5("Dengue is not Uncommon in the Philippines",
                            style={"color": "black"}),
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
                    html.H5("The Vital Role of Accessible Healthcare",
                            style={"color": "black"}),
                    html.P("The World Health Organization (2022) emphasizes that timely medical care and early detection can reduce dengue fatality rates to less than 1%. Research by Lum et al. (2014) underscores the significance of basic primary care access in mitigating dengue-related morbidity and mortality. Freitas et al. (2019) further support this, revealing that inadequate healthcare access leads to delayed treatment, with 90% of dengue fatalities occurring due to late admission to medical facilities in areas with limited healthcare infrastructure.", style={
                        'text-align': 'justify'}),
                ], width=8),
                ]),
        html.Br(),
        html.Br(),

        dbc.Row([
                dbc.Col([
                    html.H5("Our goal for this Project:",
                            style={"color": "black"}),
                    html.P("Our project aims to shed light on the severity of Dengue in the regions and cities of the Philippines. Through visualizations - the use of graphs, charts, and maps, we will illustrate the incidence of dengue cases, deaths, and fatality rates across different cities, allowing for comparisons to identify the most and least affected areas. Additionally, we intend to identify notable regions with high and low dengue fatality rates to establish focal points for further investigation and intervention efforts.  By utilizing data visualization techniques, we aim to not only raise awareness about the pressing healthcare challenges faced by certain communities but also to inform targeted interventions aimed at mitigating the impact of dengue outbreaks in the Philippines.", style={
                        'text-align': 'justify'})
                ], width=8),
                dbc.Col([
                    html.Img(
                        src="https://github.com/R3NZ3L/DATA101-Final-Project/blob/main/assets/person_picture3.jpg?raw=true", style={'width': '100%'}),
                ], width=4),
                ]),

        html.Br(),

        html.Hr(),

        dbc.Row([
            html.Div([
                html.H4("Severity of Dengue Across the Philippines", style={
                    'text-align': 'left',
                    "padding-top": '60px',
                    "padding-bottom": '10px',
                    "color": "black"

                }),
                html.P("The interactive map on the bottom left presents the severity of dengue in the Philippines. Select the depth of the data whether regional or provincial on the radio buttons. There is also an option on selecting which variable you wish to access. There are options of obtaining dengue cases, deaths, and fatality rates. The bar graph on the bottom right depicts the same data but provides a point of comparison between the areas in the country. Both in the interactive Map and Bar Chart, are levels of dengue severity in terms of the saturation of red. The more severe dengue is in an area, the more saturated the color will be.", style={
                    'text-align': 'justify',
                    "padding-bottom": '15px'
                })
            ])
        ]),


        # Visualizations
        dbc.Row([
            # Map
            dbc.Col([
                dcc.Graph(
                    figure={},
                    id='bc_map'
                )
            ], width=4),

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
                    dbc.Col([], width=3),
                    dbc.Col([
                        html.H5("Select Regions:"),
                        dcc.Dropdown(
                            id='bc_reg_dropdown_1',
                            options=bc_region_dropdown_options,
                            value='BARMM',
                            clearable=False
                        ),
                        dcc.Dropdown(
                            id='bc_reg_dropdown_2',
                            options=bc_region_dropdown_options,
                            value='CAR',
                            clearable=False
                        ),
                        dcc.Dropdown(
                            id='bc_reg_dropdown_3',
                            options=bc_region_dropdown_options,
                            value='MIMAROPA',
                            clearable=False
                        )
                    ], width=3),
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
            ], width=8)
        ]),

        html.Br(),
        html.Hr(),
        dbc.Row([
            html.Div([
                html.H4("Dengue Severity Across Time", style={
                    'text-align': 'left',
                    "padding-top": '60px',
                    "padding-bottom": '10px',
                    "color": "black"

                }),
                html.P("The interactive line graph below presents the reported severity of Dengue in the Philippines across the months in 2020. Select the depth of the data whether national or regional on the radio buttons. There is also an option on selecting which variables and regions you wish to access. There are options of obtaining dengue cases and deaths by selecting the radio buttons, and the dropdown provides a method of isolating a specific region that you wish to highlight. Additionally, the graph legend on the right is interactive. Clicking on a region allows the attributed line to disappear or reappear. Selecting National as the depth aggregates the reported severity across all regions in the country throughout the year.", style={
                    'text-align': 'justify',
                    "padding-bottom": '15px'
                })
            ])
        ]),
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
    Input("variable", "value"),
    Input("bc_reg_dropdown_1", "value"),
    Input("bc_reg_dropdown_2", "value"),
    Input("bc_reg_dropdown_3", "value")
)
def update_bc_bar(map_depth, variable, prov1, prov2, prov3):
    provs = [prov1, prov2, prov3]

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

    return fig.update_layout(margin=dict(t=20, b=50), height=400)


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
                labels={"cases": "Number of Cases"},
                center={"lat": 12.74, "lon": 120.9803},
                mapbox_style="open-street-map",
                zoom=4.335
            )
        elif variable == "deaths":
            fig = px.choropleth_mapbox(
                regions_gdf,
                geojson=regions_gdf.geometry,
                locations=regions_gdf.index,
                color="deaths",
                color_continuous_scale=px.colors.sequential.OrRd,
                labels={"cases": "Number of Deaths"},
                center={"lat": 12.74, "lon": 120.9803},
                mapbox_style="open-street-map",
                zoom=4.335
            )
        elif variable == "fatality_rate":
            fig = px.choropleth_mapbox(
                regions_gdf,
                geojson=regions_gdf.geometry,
                locations=regions_gdf.index,
                color="fatality_rate",
                color_continuous_scale=px.colors.sequential.OrRd,
                labels={"cases": "Fatality Rate (in %)"},
                center={"lat": 12.74, "lon": 120.9803},
                mapbox_style="open-street-map",
                zoom=4.335
            )

    elif map_depth == "province":
        pass

    return fig.update_layout(coloraxis_showscale=False, mapbox_bounds={"west": 110, "east": 130, "south": 0, "north": 25},
                             margin=dict(t=20, b=50, l=0, r=0), height=550)


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
                          title=f"Dengue {line_variable} Across The Regions Throughout 2020",
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
                          title=f"Dengue {line_variable} in {region_dropdown} Throughout 2020",
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
                      title=f"National Aggregate {line_variable} in the Philippines throughout 2020",
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
    app.run(debug=True)
