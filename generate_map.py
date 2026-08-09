import pydeck as pdk
import pandas as pd
import os

csv_filename = "dortmund_gebaeude.csv"

# 1. Testdaten erzeugen, falls Datei fehlt
if not os.path.exists(csv_filename):
    test_data = {
        'lng': [7.4653, 7.4680, 7.4610, 7.4635],
        'lat': [51.5136, 51.5145, 51.5125, 51.5150],
        'height': [45, 20, 35, 12]
    }
    pd.DataFrame(test_data).to_csv(csv_filename, index=False)

data = pd.read_csv(csv_filename)

# ========================================================
# REPARATUR: get_tile_data gelöscht, um Parser-Absturz zu verhindern!
# ========================================================
background_map_layer = pdk.Layer(
    "TileLayer",
    # Die exakte Adresse für die Carto-Dunkelkarte
    "https://cartocdn.com{z}/{x}/{y}.png",
    id="base-map-tiles",
    min_zoom=0,
    max_zoom=20,
    tile_size=256,
)

# 2. Ihre 3D-Gebäude-Ebene
building_layer = pdk.Layer(
    "ColumnLayer",
    data,
    get_position="[lng, lat]",
    get_elevation="height",
    get_fill_color="[200, 30, 0, 160]",
    radius=25,
    elevation_scale=1,
    extruded=True,
    pickable=True,
)

# 3. Kartenansicht
view_state = pdk.ViewState(
    latitude=51.5136, 
    longitude=7.4653, 
    zoom=14.5, 
    pitch=45,
    bearing=10
)

# 4. Render und Export (Wir schalten den internen Pydeck-Provider komplett AUS)
r = pdk.Deck(
    # WICHTIG: Die Karte liegt als allererste Ebene UNTER den Gebäuden
    layers=[background_map_layer, building_layer], 
    initial_view_state=view_state,
    map_provider=None,  # Schaltet fehlerhafte Pydeck-Automatismen & Mapbox ab!
    map_style=None      # Deaktiviert interne Styles
)

output_html = "option4_pydeck.html"
r.to_html(output_html)
print(f"Erfolgreich! Die Datei '{output_html}' wurde mit eigener Tile-Map exportiert.")