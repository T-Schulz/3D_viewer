import pydeck as pdk
import pandas as pd

# Angenommen, Sie haben die DXF-Daten in eine CSV-Tabelle extrahiert
# mit den Spalten: 'lng', 'lat', 'height' (Gebäudehöhe)
data = pd.read_csv("dortmund_gebaeude.csv")

# 3D-Gebäude-Ebene definieren
layer = pdk.Layer(
    "PolygonLayer",  # Oder ColumnLayer/MeshLayer je nach Datenstruktur
    data,
    get_polygon="-", # Geometriedaten der Grundrisse
    get_elevation="height",
    get_fill_color="[200, 30, 0, 160]",
    elevation_scale=1,
    extruded=True,
)

# Kartenansicht auf Dortmund zentrieren
view_state = pdk.ViewState(latitude=51.5136, longitude=7.4653, zoom=14, pitch=45)

# Render und Export als HTML-Datei
r = pdk.Deck(layers=[layer], initial_view_state=view_state)
r.to_html("option4_pydeck.html") 