import streamlit as st
import folium
from shapely.geometry import shape
import fiona
import pandas as pd
from streamlit_folium import st_folium
from folium.plugins import HeatMap

def main():
    st.title("Heatmap Berlin")

    # Dropdown-Menü für die Auswahl der Karte
    map_style = st.selectbox(
        "Wähle eine Kartenansicht aus:",
        ["OpenStreetMap", "Stamen Toner", "CartoDB Positron", "CartoDB Dark Matter"]
    )

    # Shapefile der Bezirksgrenzen laden
    shapefile_path = r'C:\Users\marce\Desktop\bezirksgrenzen.shp'
    
    # Bezirksgrenzen laden und als geometrische Objekte speichern
    shapes = []
    districts = []
    with fiona.open(shapefile_path, 'r') as shapefile:
        for feature in shapefile:
            shapes.append(shape(feature['geometry']))
            districts.append(feature['properties']['Gemeinde_n'])

    # Kriminalitätsdaten laden (CSV-Datei mit Verbrechen pro Bezirk)
    crime_data_path = r'C:\Users\marce\Desktop\Bezirke 14-26.csv'
    df_crime = pd.read_csv(crime_data_path)
    
    # Filteroptionen für Jahre und Straftaten hinzufügen
    st.sidebar.header("Filteroptionen")
    selected_year = st.sidebar.selectbox("Wähle ein Jahr aus:", df_crime['Jahr'].unique())
    min_crime = st.sidebar.number_input("Minimale Anzahl an Straftaten:", min_value=0, value=0)
    max_crime = st.sidebar.number_input("Maximale Anzahl an Straftaten:", min_value=0, value=100000)
    
    # Eingabefelder für die Schwellenwerte der Farbcodierung
    st.sidebar.header("Farbcodierung anpassen")
    red_threshold = st.sidebar.number_input("Schwellenwert für Rot (>):", min_value=0, value=40000)
    orange_threshold = st.sidebar.number_input("Schwellenwert für Orange (>):", min_value=0, value=30000)

    # Daten nach ausgewähltem Jahr filtern
    df_crime_filtered = df_crime[(df_crime['Jahr'] == selected_year) & 
                                 (df_crime['Straftaten(insgesamt)'] >= min_crime) & 
                                 (df_crime['Straftaten(insgesamt)'] <= max_crime)]
    
    # Namen bereinigen: Leerzeichen entfernen und Kleinbuchstaben verwenden
    df_crime_filtered['Bezirk_normalized'] = df_crime_filtered['Bezeichnung_(Bezirksregion)'].str.strip().str.lower()
    districts_normalized = [district.strip().lower() for district in districts]

    # Erstellung der Karte mit der gewählten Kartenansicht
    attribution = {
        "OpenStreetMap": "© OpenStreetMap contributors",
        "Stamen Toner": "Map tiles by Stamen Design, under CC BY 3.0. Data by OpenStreetMap, under ODbL.",
        "CartoDB Positron": "Map tiles by Carto, under CC BY 3.0. Data by OpenStreetMap, under ODbL.",
        "CartoDB Dark Matter": "Map tiles by Carto, under CC BY 3.0. Data by OpenStreetMap, under ODbL."
    }

    m = folium.Map(location=[52.5200, 13.4050], zoom_start=10, tiles=map_style, attr=attribution[map_style])
    
    # Polygone zur Karte hinzufügen und nach Kriminalitätsdaten farbcodieren
    for i, polygon in enumerate(shapes):
        district_name = districts_normalized[i]
        crime_row = df_crime_filtered[df_crime_filtered['Bezirk_normalized'] == district_name]
        
        if not crime_row.empty:
            crime_count = crime_row['Straftaten(insgesamt)'].values[0]
            percent_change = crime_row['Prozentualle_Veränderung_zum_Vorjahr'].values[0]
        else:
            crime_count = 0
            percent_change = "Keine Daten"

        # Farbcodierung basierend auf der Anzahl der Verbrechen und benutzerdefinierten Schwellenwerten
        if crime_count > red_threshold:
            color = 'red'
        elif crime_count > orange_threshold:
            color = 'orange'
        else:
            color = 'green'

        # Popup-Text und Tooltip-Text für den Bezirk, einschließlich der prozentualen Veränderung zum Vorjahr
        popup_text = f"{districts[i]}: {crime_count} Straftaten<br>Veränderung zum Vorjahr: {percent_change}%"
        tooltip_text = f"{districts[i]}"

        # Polygon zur Karte hinzufügen mit Popup und Tooltip
        folium.GeoJson(
            polygon,
            style_function=lambda x, color=color: {
                'fillColor': color,
                'color': 'black',
                'weight': 2,
                'fillOpacity': 0.5
            },
            tooltip=tooltip_text,
            popup=folium.Popup(popup_text, max_width=300)
        ).add_to(m)
    
    # Optional: Heatmap auf Basis der Verbrechen hinzufügen, wenn Koordinaten verfügbar sind
    if 'Lat' in df_crime_filtered.columns and 'Lon' in df_crime_filtered.columns:
        heat_data = [[row['Lat'], row['Lon']] for index, row in df_crime_filtered.iterrows()]
        HeatMap(heat_data).add_to(m)
    
    # Karte in Streamlit anzeigen
    st_folium(m)

if __name__ == '__main__':
    main()
