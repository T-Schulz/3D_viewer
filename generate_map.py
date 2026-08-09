import pydeck as pdk
import pandas as pd
import os

# 1. Sicherstellen, dass die CSV-Datei existiert (sonst erstellen wir Testdaten für Dortmund)
csv_filename = "dortmund_gebaeude.csv"

if not os.path.exists(csv_filename):
    print(f"'{csv_filename}' nicht gefunden. Erstelle automatische Testdaten...")
    # 4 Gebäude im Dortmunder Zentrum (Nähe Reinoldikirche / U-Turm)
    test_data = {
        'lng': [7.4653, 7.4680, 7.4610, 7.4635],
        'lat': [51.5136, 51.5145, 51.5125, 51.5150],
        'height': [25, 45, 15, 30] # Gebäudehöhen in Metern
    }
    df = pd.DataFrame(test_data)
    df.to_csv(csv_filename, index=False)

# 2. Reale oder generierte CSV-Daten einlesen
data = pd.read_csv(csv_filename)

# 3. 3D-Säulen-Ebene definieren (Perfekt für lng/lat-Punktdaten)
layer = pdk.Layer(
    "ColumnLayer",
    data,
    get_position="[lng, lat]",     # Extrahiert Längengrad und Breitengrad
    get_elevation="height",         # Nutzt die Spalte 'height' für die 3D-Höhe
    get_fill_color="[200, 30, 0, 160]", # Rötliche, leicht transparente Blöcke
    radius=25,                      # Breite/Radius der 3D-Blöcke in Metern
    elevation_scale=1,
    extruded=True,                  # Aktiviert den 3D-Effekt
    pickable=True,
)

# 4. Kartenansicht auf Dortmund zentrieren
view_state = pdk.ViewState(
    latitude=51.5136, 
    longitude=7.4653, 
    zoom=14.5, 
    pitch=45,
    bearing=10
)

# 5. Render und Export als HTML-Datei (Korrektur: map_provider hinzugefügt!)
r = pdk.Deck(
    layers=[layer], 
    initial_view_state=view_state,
    map_provider="mapbox", # Zwingend erforderlich bei benutzerdefinierten Dict-Styles!
    map_style={
        "version": 8,
        "sources": {
            "carto-tiles": {
                "type": "raster",
                "tiles": [
                    "https://cartocdn.com{z}/{x}/{y}.png",
                    "https://cartocdn.com{z}/{x}/{y}.png"
                ],
                "tileSize": 256
            }
        },
        "layers": [
            {
                "id": "carto-layer",
                "type": "raster",
                "source": "carto-tiles",
                "minzoom": 0,
                "maxzoom": 20
            }
        ]
    }
)

output_html = "option4_pydeck.html"
r.to_html(output_html)
print(f"Erfolgreich! Die Datei '{output_html}' wurde ohne Token-Zwang generiert.")