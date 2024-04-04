from dash import Dash, html, dash_table, dcc, callback, Output, Input
import dash_bootstrap_components as dbc

external_stylesheets = [dbc.themes.MINTY]
app = Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "GROUP A - DATA101 Final Project"

app.layout = dbc.Container([
    # Navigation Bar
    dbc.NavbarSimple([
        dbc.NavItem(dbc.NavLink("BACKGROUND", href="#")),
        dbc.NavItem(dbc.NavLink("VISUALIZATIONS", href="#")),
        dbc.NavItem(dbc.NavLink("APAYAO", href="#"))
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
    ])
])

if __name__ == '__main__':
    app.run_server(debug=True, port=8051)
