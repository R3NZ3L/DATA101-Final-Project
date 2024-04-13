# Philippine Dengue Severity Dashboard (Group A)
 
Authors:
- ALDECOA, Renzel
- BANICO, Adrian
- NAVARRO, Carl; and
- SAMSON, Romm

This repository contains our final project for DATA101.

Our project aims to shed light on the severity of Dengue in the regions and cities of the Philippines. Through visualizations - the use of graphs, charts, and maps, we will illustrate the incidence of dengue cases, deaths, and fatality rates across different cities, allowing for comparisons to identify the most and least affected areas. We visualized the severity of Dengue across provinces and regions, as well as over time (in the year 2020).

### Setup Instructions
Our dashboard uses the following libraries: <br>
- dash
- pandas
- plotly
- dash_bootstrap_components
- geopandas; and
- mapboxgl
<br>

To install these libraries, you can use the command below in your terminal (preferably in a virtual environment): <br>
```pip install dash pandas plotly dash_bootstrap_components geopandas mapboxgl``` <br> <br>

The file `app.py` contains the Dash application. To view our dashboard, simply run this file, starting the Flask server via Dash's libraries. <br> <br>
Once the server is up and running, the dashboard is accessible on port `8050`, the default for Dash applications <br> (NOTE: please vacate this port before running or specify a port number in the source code). <br> <br>
Once accessible, you will arrive at our landing page. From there, our visualizations are accessible by scrolling down.
