import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np
from sklearn.linear_model import LinearRegression

def main():
           
    # Laden der Daten
    data = pd.read_csv("Bezirke 14-23 - Rohdaten.csv")
    
    # Mittig ausgerichtetes Dropdown-Menü
    col1, col2, col3 = st.columns([1, 2, 1])  # Drei Spalten erstellen
    with col2:
        category = st.selectbox("Wählen Sie eine Kategorie zur Analyse:", data.columns[1:-1])

    # Trendanalyse für die ausgewählte Kategorie
    def trend_analysis(data, category):
        plt.figure(figsize=(10, 6))
        colors = plt.cm.tab10.colors  # Farben für die Bezirke festlegen
        for i, bezirk in enumerate(data['Bezeichnung_(Bezirksregion)'].unique()):
            bezirk_data = data[data['Bezeichnung_(Bezirksregion)'] == bezirk]
            plt.plot(bezirk_data['Jahr'], bezirk_data[category], label=bezirk, color=colors[i % len(colors)])
        
        plt.title(f'Trendanalyse für {category} über die Jahre')
        plt.xlabel('Jahr')
        plt.ylabel(f'{category}')
        plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3)
        plt.tight_layout()  # Sorgt dafür, dass alles gut platziert ist
        st.pyplot(plt)
    
    # Mittig ausgerichteter Titel für Trendanalyse
    st.markdown("<h1 style='text-align: center;'>Trendanalyse von 2014-2023</h1>", unsafe_allow_html=True)
    trend_analysis(data, category)

    # Vergleich der Bezirke für die ausgewählte Kategorie
    def compare_districts(data, category):
        # Daten für Plotly vorbereiten
        district_means = data.groupby('Bezeichnung_(Bezirksregion)')[category].mean().sort_values()
        fig = px.bar(district_means, 
                     x=district_means.index, 
                     y=district_means.values, 
                     title=f'Vergleich von {category} über Bezirke hinweg',
                     labels={'y': f'Durchschnittliche {category}', 'x': 'Bezirk'})
        
        # Titel des Diagramms mittig ausrichten
        fig.update_layout(
            title={
                'text': f'Vergleich von {category} über Bezirke hinweg',
                'x': 0.5,  # Zentriert den Titel
                'xanchor': 'center',
                'yanchor': 'top'
            },
            xaxis_title=None,
            showlegend=False
        )
        st.plotly_chart(fig)
    
    # Mittig ausgerichteter Titel für Vergleich
    st.markdown("<h1 style='text-align: center;'>Vergleich der Kriminalität über Bezirke hinweg</h1>", unsafe_allow_html=True)
    compare_districts(data, category)

if __name__ == "__main__":
    main()
