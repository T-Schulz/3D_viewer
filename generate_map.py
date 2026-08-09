import pydeck as pdk
import pandas as pd
import os

csv_filename = "dortmund_gebaeude.csv"

if not os.path.exists(csv_filename):
    test_data = {
        'lng': [7.4653, 7.4680, 7.4610, 7.4635],
        'lat': [51.5136, 51.5145, 51.5125, 51.5150],
        'height': [45, 12, 28, 35]
    }
    pd.DataFrame(test_data).to_csv(csv_filename, index=False)

data = pd.read_csv(csv_filename)

# Nur die Gebäude werden in Python definiert
building_layer = pdk.Layer(
    "ColumnLayer",
    data,
    get_position="[lng, lat]",
    get_elevation="height",
    get_fill_color="[200, 30, 0, 200]",
    radius=25,
    elevation_scale=1,
    extruded=True,
    pickable=True,
)

view_state = pdk.ViewState(
    latitude=51.5136, 
    longitude=7.4653, 
    zoom=14.5, 
    pitch=45,
    bearing=10
)

# Wir exportieren NUR die Gebäude ohne jeden fehlerhaften Kartenhintergrund
r = pdk.Deck(
    layers=[building_layer], 
    initial_view_state=view_state,
    map_provider=None,
    map_style=None
)

output_html = "option4_pydeck.html"
r.to_html(output_html)
print(f"Schritt 1 erfolgreich: '{output_html}' generiert.")