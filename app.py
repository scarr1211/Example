from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd

# 1. Mock street data for Mason City, Iowa (Coordinates centered around Mason City)
data = {
    "Street": [
        "Federal Ave", 
        "State St", 
        "1st St SE", 
        "Southbridge Dr", 
        "Kossuth St", 
        "Monroe Ave", 
        "CGW Railroad / 19th St SW"
    ],
    "Lat": [43.1536, 43.1512, 43.1525, 43.1430, 43.1590, 43.1480, 43.1360],
    "Lon": [-93.2010, -93.2015, -93.1990, -93.2050, -93.2100, -93.1950, -93.2200],
    "Description": [
        "Major north-south downtown thoroughfare",
        "Historic downtown corridor",
        "Heart of downtown near cultural sites",
        "Commercial and shopping area near the mall",
        "Residential and local connector",
        "East side neighborhood road",
        "Southwest industrial / transit area"
    ]
}

df = pd.DataFrame(data)

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
            options=[{"label": s, "value": s} for s in df["Street"]],
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
    # Filter dataframe if a street is selected, otherwise show all
    if selected_street:
        filtered_df = df[df["Street"] == selected_street]
        zoom_level = 15
    else:
        filtered_df = df
        zoom_level = 12

    # Build a scatter mapbox graph using open-source OpenStreetMap tiles
    fig = px.scatter_mapbox(
        filtered_df,
        lat="Lat",
        lon="Lon",
        hover_name="Street",
        hover_data=["Description"],
        zoom=zoom_level,
        height=500
    )
    
    # Use standard open-source layout styling so no Mapbox token is required
    fig.update_layout(
        mapbox_style="open-street-map",
        margin={"r": 0, "t": 0, "l": 0, "b": 0}
    )
    
    # Center map over Mason City, Iowa coordinates if nothing selected
    if not selected_street:
        fig.update_layout(
            mapbox_center={"lat": 43.1536, "lon": -93.2010}
        )
        
    return fig

# 5. Run local server if executed directly
if __name__ == "__main__":
    app.run(debug=True)