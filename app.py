from dash import Dash, html, dcc, Input, Output
import plotly.graph_objects as go

# 1. Pure Python lists for Mason City data
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

# 2. Initialize the Dash app and expose the Flask server
app = Dash(__name__)
server = app.server  # <--- This is what Gunicorn needs to call!

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
        center_lat = f_lats[0]
        center_lon = f_lons[0]
    else:
        f_streets = streets
        f_lats = lats
        f_lons = lons
        f_descs = descriptions
        zoom_level = 12
        center_lat = 43.1536
        center_lon = -93.2010

    fig = go.Figure(
        go.Scattermapbox(
            lat=f_lats,
            lon=f_lons,
            mode="markers+text",
            marker=dict(size=14, color="#e74c3c"),
            text=f_streets,
            textposition="top right",
            customdata=f_descs,
            hovertemplate="<b>%{text}</b><br>%{customdata}<extra></extra>"
        )
    )
    
    fig.update_layout(
        mapbox_style="open-street-map",
        mapbox=dict(
            center=dict(lat=center_lat, lon=center_lon),
            zoom=zoom_level
        ),
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        height=500
    )
        
    return fig

if __name__ == "__main__":
    app.run(debug=True)