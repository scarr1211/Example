from dash import Dash, html, dcc, Input, Output
import plotly.express as px

# 1. Pure Python lists for Mason City data (No pandas/numpy required!)
streets = [
    "Federal Ave", 
    "State St", 
    "1st St SE", 
    "Southbridge Dr", 
    "Kossuth St", 
    "Monroe Ave", 
    "CGW Railroad / 19th St SW"
]
lats = [43.1536, 43.1512, 43.1525, 43.1430, 43.1590, 43.1480, 43.1360]
lons = [-93.2010, -93.2015, -93.1990, -93.2050, -93.2100, -93.1950, -93.2200]
descriptions = [
    "Major north-south downtown thoroughfare",
    "Historic downtown corridor",
    "Heart of downtown near cultural sites",
    "Commercial and shopping area near the mall",
    "Residential and local connector",
    "East side neighborhood road",
    "Southwest industrial / transit area"
]

# 2. Initialize the Dash app
app = Dash(__name__)
server = app.server  # Required for Render deployment

# 3. Design the layout
app.layout = html.Div(
    style={"fontFamily": "Arial, sans-serif", "margin": "20px", "maxWidth": "900px", "marginAuto": "auto"},
    children=[
        html.H1("Mason City, Iowa - Street Finder Dashboard", style={"color": "#2c3e50"}),
        html.P("Type a street name below to filter the map view of Mason City."),
        
        # Search / Dropdown input box
        html.Label("Search or Select Street:"),
        dcc.Dropdown(
            id="street-dropdown",
            options=[{"label": s, "value": s} for s in streets],
            value=None,
            placeholder="Type a street name (e.g., Federal Ave)...",
            clearable=True,
            style={"marginBottom": "20px"}
        ),
        
        # Map Display component
        dcc.Graph(id="mason-city-map")
    ]
)

# 4. Create the interactivity callback
@app.callback(
    Output("mason-city-map", "figure"),
    Input("street-dropdown", "value")
)
def update_map(selected_street):
    if selected_street:
        idx = streets.index(selected_street)
        f_streets = [streets[idx]]
        f_lats = [lats[idx]]
        f_lons = [lons[idx]]
        f_descs = [descriptions[idx]]
        zoom_level = 15
    else:
        f_streets = streets
        f_lats = lats
        f_lons = lons
        f_descs = descriptions
        zoom_level = 12

    # Build scatter mapbox using pure lists
    fig = px.scatter_mapbox(
        lat=f_lats,
        lon=f_lons,
        hover_name=f_streets,
        custom_data=[f_descs],
        zoom=zoom_level,
        height=500
    )
    
    fig.update_traces(
        hovertemplate="<b>%{hovername}</b><br>%{customdata[0]}<extra></extra>"
    )
    
    fig.update_layout(
        mapbox_style="open-street-map",
        margin={"r": 0, "t": 0, "l": 0, "b": 0}
    )
    
    if not selected_street:
        fig.update_layout(
            mapbox_center={"lat": 43.1536, "lon": -93.2010}
        )
        
    return fig

if __name__ == "__main__":
    app.run(debug=True)