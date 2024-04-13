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
hospitals = gpd.read_file("datasets/shapefiles/hospitals/hospitals.shp")

temp_reg_code = {'REGION IX (ZAMBOANGA PENINSULA)': 900000000,
                 'Bangsamoro Autonomous Region In Muslim Mindanao (BARMM)': 1900000000,
                 'Region X (northern Mindanao)': 1000000000,
                 'REGION XII (SOCCSKSARGEN)': 1200000000,
                 'REGION VII (CENTRAL VISAYAS)': 700000000,
                 'CAR (CORDILLERA ADMINISTRATIVE REGION': 1400000000,
                 'REGION VI (WESTERN VISAYAS)': 600000000,
                 'REGION IV-B (MIMAROPA)': 1700000000,
                 'REGION VIII (EASTERN VISAYAS)': 800000000,
                 'REGION II (CAGAYAN VALLEY)': 200000000,
                 'REGION XIII (CARAGA)': 1600000000,
                 'REGION III (CENTRAL LUZON)': 300000000,
                 'REGION V (BICOL REGION)': 500000000,
                 'REGION I (ILOCOS REGION)': 100000000,
                 'REGION IV-A (CALABARZON)': 400000000,
                 'NCR (NATIONAL CAPITAL REGION)': 1300000000,
                 'REGION XI (DAVAO REGION)': 1100000000}

temp_reg_name = {'REGION IX (ZAMBOANGA PENINSULA)': 'Region IX (Zamboanga Peninsula)',
                 'Region X (northern Mindanao)': 'Region X (Northern Mindanao)',
                 'REGION XII (SOCCSKSARGEN)': 'Region XII (SOCCSKSARGEN)',
                 'REGION VII (CENTRAL VISAYAS)': 'Region VII (Central Visayas)',
                 'CAR (CORDILLERA ADMINISTRATIVE REGION': 'Cordillera Administrative Region (CAR)',
                 'REGION VI (WESTERN VISAYAS)': 'Region VI (Western Visayas)',
                 'REGION IV-B (MIMAROPA)': 'MIMAROPA Region',
                 'REGION VIII (EASTERN VISAYAS)': 'Region VIII (Eastern Visayas)',
                 'REGION II (CAGAYAN VALLEY)': 'Region II (Cagayan Valley)',
                 'REGION XIII (CARAGA)': 'Region XIII (Caraga)',
                 'REGION III (CENTRAL LUZON)': 'Region III (Central Luzon)',
                 'REGION V (BICOL REGION)': 'Region V (Bicol Region)',
                 'REGION I (ILOCOS REGION)': 'Region I (Ilocos Region)',
                 'REGION IV-A (CALABARZON)': 'Region IV-A (CALABARZON)',
                 'NCR (NATIONAL CAPITAL REGION)': 'National Capital Region (NCR)',
                 'REGION XI (DAVAO REGION)': 'Region XI (Davao Region)'}

temp_list = []
for i in range(hospitals.shape[0]):
    temp_list.append(temp_reg_code.get(hospitals.iloc[i]["region"]))

hospitals["region"] = hospitals["region"].map(temp_reg_name)
hospitals.insert(6, "adm1_psgc", temp_list)

regions_gdf = regions[["adm1_psgc", "geometry"]].merge(
    cdpr, on="adm1_psgc").set_index("adm1_psgc")
provinces_gdf = provinces[["adm2_psgc", "geometry"]].merge(
    cdpp, on="adm2_psgc").set_index("adm2_psgc")
hospitals_gdf = hospitals[["healthfaci", "adm1_psgc", "geometry"]].merge(
    cdpp, on="adm1_psgc").set_index("adm1_psgc")

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
    dbc.NavbarSimple(
        [
            dbc.NavItem(dbc.NavLink("Background", href="#")),
            dbc.NavItem(dbc.NavLink(
                "Across The Philippines", href="#across_country")),
            dbc.NavItem(dbc.NavLink("Across Time", href="#across_time")),
            dbc.NavItem(dbc.NavLink("Hospitals in the Philippines", href="#hospitals"))
        ],
        brand="GROUP A - Final Project",
        brand_href="#",
        color="#FFF9C4",
        sticky="top",
        # Make the navbar stick to the top of the page
        style={'height': '60px'},
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
            ["There were ", html.Strong("91,000+", style={'color': '#D32F2F', 'text-shadow': '1px 1px 1px black'}),
             " confirmed dengue infections and ", html.Strong(
                "1,100+", style={'color': '#D32F2F', 'text-shadow': '1px 1px 1px black'}), " confirmed deaths from ",
             html.Strong("Dengue", style={'color': '#D32F2F', 'text-shadow': '1px 1px 1px black'}), " in 2020 "],
            style={
                'padding': '20px',
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
                html.P(
                    "Every year, tens and even hundreds of thousands of Filipinos contract this illness, and many succumb to it. The 2019 dengue outbreak was one of the worst years for the country, wherein it has reported the highest number of cases and deaths across Southeast Asia (Santos, 2019). The impact was severe, with over 370,000 cases, and 1400 casualties recorded in a single year (World Health Organization, 2019).",
                    style={
                        'text-align': 'justify'})
            ], width=8),
            dbc.Col([
                html.Img(
                    src="https://github.com/R3NZ3L/DATA101-Final-Project/blob/main/assets/hospital_picture1.jpg?raw=true",
                    style={'width': '100%'}),
            ], width=4),
        ]),

        html.Br(),
        html.Br(),

        dbc.Row([
            dbc.Col([
                html.Img(
                    src="https://github.com/R3NZ3L/DATA101-Final-Project/blob/main/assets/hospital_picture2.png?raw=true",
                    style={'width': '100%'}),
            ], width=4),
            dbc.Col([
                html.H5("The Vital Role of Accessible Healthcare",
                        style={"color": "black"}),
                html.P(
                    "The World Health Organization (2022) emphasizes that timely medical care and early detection can reduce dengue fatality rates to less than 1%. Research by Lum et al. (2014) underscores the significance of basic primary care access in mitigating dengue-related morbidity and mortality. Freitas et al. (2019) further support this, revealing that inadequate healthcare access leads to delayed treatment, with 90% of dengue fatalities occurring due to late admission to medical facilities in areas with limited healthcare infrastructure.",
                    style={
                        'text-align': 'justify'}),
            ], width=8),
        ]),

        html.Br(),
        html.Br(),

        dbc.Row([
            dbc.Col([
                html.H5("Our goal for this Project:",
                        style={"color": "black"}),
                html.P(
                    "Our project aims to shed light on the severity of Dengue in the regions and cities of the Philippines. Through visualizations - the use of graphs, charts, and maps, we will illustrate the incidence of dengue cases, deaths, and fatality rates across different cities, allowing for comparisons to identify the most and least affected areas. Additionally, we intend to identify notable regions with high and low dengue fatality rates to establish focal points for further investigation and intervention efforts.  By utilizing data visualization techniques, we aim to not only raise awareness about the pressing healthcare challenges faced by certain communities but also to inform targeted interventions aimed at mitigating the impact of dengue outbreaks in the Philippines.",
                    style={
                        'text-align': 'justify'})
            ], width=8),
            dbc.Col([
                html.Img(
                    src="https://github.com/R3NZ3L/DATA101-Final-Project/blob/main/assets/person_picture3.jpg?raw=true",
                    style={'width': '100%'}),
            ], width=4),
        ]),

        html.Br(),

        html.Hr(),

        dbc.Row(
            id="across_country",  # Assigning the id attribute
            children=[
                html.Div(
                    [
                        html.H4("Severity of Dengue Across the Philippines", style={
                            'text-align': 'left',
                            "padding-top": '60px',
                            "padding-bottom": '10px',
                            "color": "black"
                        }),
                        html.P(
                            "The interactive map on the bottom left presents the severity of dengue in the Philippines. Select the depth of the data whether regional or provincial on the radio buttons. There is also an option on selecting which variable you wish to access. There are options of obtaining dengue cases, deaths, and fatality rates. The bar graph on the bottom right depicts the same data but provides a point of comparison between the areas in the country. Both in the interactive Map and Bar Chart, are levels of dengue severity in terms of the saturation of red. The more severe dengue is in an area, the more saturated the color will be. Additionally with the option to select 3 regions on the dropdown, the map will update to show provincial boundaries and a choropleth depending on the selected variable, this too reflects on the bar graph wherein the severity of dengue is presented in order of severity and grouped by regions.",
                            style={
                                'text-align': 'justify',
                                "padding-bottom": '15px'
                            })
                    ]
                )
            ]),

        # Visualizations
        dbc.Row([
            # Map
            dbc.Col([
                dcc.Graph(
                    figure={},
                    id='bc_map'
                )
            ], width=5),

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
            ], width=7)
        ]),

        html.Br(),
        html.Hr(),
        dbc.Row(
            id="across_time",
            children=[
                html.Div([
                    html.H4("Severity of Dengue Across Time", style={
                        'text-align': 'left',
                        "padding-top": '60px',
                        "padding-bottom": '10px',
                        "color": "black"
                    }),
                    html.P(
                        "The interactive line graph below presents the reported severity of Dengue in the Philippines across the months in 2020. Select the depth of the data whether national or regional on the radio buttons. There is also an option on selecting which variables and regions you wish to access. There are options of obtaining dengue cases and deaths by selecting the radio buttons, and the dropdown provides a method of isolating a specific region that you wish to highlight. Additionally, the graph legend on the right is interactive. Clicking on a region allows the attributed line to disappear or reappear. Selecting National as the depth aggregates the reported severity across all regions in the country throughout the year.",
                        style={
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
        ]),

        html.Hr(),

        dbc.Row(
            id="hospitals",  # Assigning the id attribute
            children=[
                html.Div(
                    [
                        html.H4("Location of Hospitals in the Philippines", style={
                            'text-align': 'left',
                            "padding-top": '60px',
                            "padding-bottom": '10px',
                            "color": "black"
                        }),
                        html.P(
                            "The visualization below presents the number and locations of hospitals across the Philippines as of 2020 through points on the map. The graph provides a bird's eye view on the hospitals in the country where each point represents a hospital located in the area. There are options of zooming in and out of specific areas, and panning around the map of the Philippines. When a point in the map is hovered it provides a number of information. This includes the name of the hospital, the hospital's region, and province, as well as the number of cases, deaths, and fatality rates reported in the area.",
                            style={
                                'text-align': 'justify',
                                "padding-bottom": '15px'
                            })
                    ]
                )
            ]),

        dbc.Row([
            dcc.Graph(
                figure=px.scatter_mapbox(
                    hospitals_gdf, lat=hospitals_gdf.geometry.y, lon=hospitals_gdf.geometry.x,
                    center={"lat": 12.74, "lon": 120.9803}, mapbox_style="carto-positron", zoom=3.0,
                    hover_name="healthfaci", hover_data=["region", "province", "cases", "deaths", "fatality_rate"],
                    labels={
                        "region": "Region",
                        "province": "Province",
                        "cases": "Number of Cases",
                        "deaths": "Number of Deaths",
                        "fatality_rate": "Fatality rate (in %)"
                    }
                ).update_layout(
                    mapbox_bounds={"west": 110, "east": 130, "south": 0, "north": 25},
                    margin=dict(t=20, b=50, l=0, r=0), height=550
                ).update_traces(
                    marker_color="#FF0A00"
                )
            )
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
def update_bc_bar(map_depth, variable, reg1, reg2, reg3):
    regs = [reg1, reg2, reg3]

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
        condition = f"(cdpp['region'] == '{regs[0]}')"
        for region in regs[1:]:
            condition += f" | (cdpp['region'] == '{region}')"

        if variable == "cases":
            fig = px.bar(
                cdpp.sort_values(
                    ascending=False, by="cases").loc[eval(condition)],
                x="province",
                y="cases",
                color="region",
                color_discrete_map=color_dict,
                labels={
                    "province": "Province",
                    "cases": "Number of Cases",
                    "region": "Region"
                },
                text_auto=True
            )
        elif variable == "deaths":
            fig = px.bar(
                cdpp.sort_values(
                    ascending=False, by="deaths").loc[eval(condition)],
                x="province",
                y="deaths",
                color="region",
                color_discrete_map=color_dict,
                labels={
                    "province": "Province",
                    "deaths": "Number of Deaths",
                    "region": "Region"
                },
                text_auto=True
            )
        elif variable == "fatality_rate":
            fig = px.bar(
                cdpp.sort_values(
                    ascending=False, by="fatality_rate").loc[eval(condition)],
                x="province",
                y="fatality_rate",
                color="region",
                color_discrete_map=color_dict,
                labels={
                    "province": "Province",
                    "fatality_rate": "Fatality Rate (in %)",
                    "region": "Region"
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
                hover_name="region",
                hover_data=["cases"],
                color="cases",
                color_continuous_scale=px.colors.sequential.OrRd,
                labels={"cases": "Number of Cases"},
                center={"lat": 12.74, "lon": 120.9803},
                mapbox_style="carto-positron",
                zoom=4.335
            )
        elif variable == "deaths":
            fig = px.choropleth_mapbox(
                regions_gdf,
                geojson=regions_gdf.geometry,
                locations=regions_gdf.index,
                hover_name="region",
                hover_data=["deaths"],
                color="deaths",
                color_continuous_scale=px.colors.sequential.OrRd,
                labels={"deaths": "Number of Deaths"},
                center={"lat": 12.74, "lon": 120.9803},
                mapbox_style="carto-positron",
                zoom=4.335
            )
        elif variable == "fatality_rate":
            fig = px.choropleth_mapbox(
                regions_gdf,
                geojson=regions_gdf.geometry,
                locations=regions_gdf.index,
                hover_name="region",
                hover_data=["fatality_rate"],
                color="fatality_rate",
                color_continuous_scale=px.colors.sequential.OrRd,
                labels={"fatality_rate": "Fatality Rate (in %)"},
                center={"lat": 12.74, "lon": 120.9803},
                mapbox_style="carto-positron",
                zoom=4.335
            )

    elif map_depth == "province":
        if variable == "cases":
            fig = px.choropleth_mapbox(
                provinces_gdf,
                geojson=provinces_gdf.geometry,
                locations=provinces_gdf.index,
                hover_name="province",
                hover_data=["cases", "region"],
                color="cases",
                color_continuous_scale=px.colors.sequential.OrRd,
                labels={"province": "Province", "region": "Region", "cases": "Number of Cases"},
                center={"lat": 12.74, "lon": 120.9803},
                mapbox_style="carto-positron",
                zoom=4.335
            )
        elif variable == "deaths":
            fig = px.choropleth_mapbox(
                provinces_gdf,
                geojson=provinces_gdf.geometry,
                locations=provinces_gdf.index,
                hover_name="province",
                hover_data=["deaths", "region"],
                color="deaths",
                color_continuous_scale=px.colors.sequential.OrRd,
                labels={"province": "Province", "region": "Region", "deaths": "Number of Deaths"},
                center={"lat": 12.74, "lon": 120.9803},
                mapbox_style="carto-positron",
                zoom=4.335
            )
        elif variable == "fatality_rate":
            fig = px.choropleth_mapbox(
                provinces_gdf,
                geojson=provinces_gdf.geometry,
                locations=provinces_gdf.index,
                hover_name="province",
                hover_data=["fatality_rate"],
                color="fatality_rate",
                color_continuous_scale=px.colors.sequential.OrRd,
                center={"lat": 12.74, "lon": 120.9803},
                mapbox_style="carto-positron",
                zoom=4.335
            )

    return fig.update_layout(mapbox_bounds={"west": 110, "east": 130, "south": 0, "north": 25},
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

    return fig.update_layout(margin=dict(b=50), height=550)


if __name__ == "__main__":
    app.run(debug=True)
