import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
import plotly.graph_objects as go

# CSS für die mittige Ausrichtung hinzufügen
st.markdown(
    """
    <style>
    .centered-content {
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
    }
    </style>
    """,
    unsafe_allow_html=True
)

def main():
    # Titel der App
    st.markdown("<h1 style='text-align: center;'>Vorhersage von Straftaten in Bezirken für die nächsten 3 Jahre</h1>", unsafe_allow_html=True)
    
    # Datei-Upload oder lokalen Dateipfad verwenden
    file_path = 'Bezirke 14-23 - Rohdaten.csv'
    data = pd.read_csv(file_path)
    
    if data is not None:
        # Mittige Anordnung aller Dropdown-Menüs und Checkboxen
        with st.container():
            st.markdown("<div class='centered-content'>", unsafe_allow_html=True)
            
            # Dropdown-Menü für die Auswahl des Bezirks
            bezirk_list = data['Bezeichnung_(Bezirksregion)'].unique()
            selected_bezirk = st.selectbox('Wähle einen Bezirk aus:', bezirk_list)
        
            # Dropdown-Menü für die Auswahl der Spalte
            spalten_list = [col for col in data.columns if col not in ['Bezeichnung_(Bezirksregion)', 'Jahr']]
            selected_spalte = st.selectbox('Wähle eine Spalte aus:', spalten_list)
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Daten für den ausgewählten Bezirk und die ausgewählte Spalte filtern
        bezirk_data = data[data['Bezeichnung_(Bezirksregion)'] == selected_bezirk]
        X_bezirk = bezirk_data[['Jahr']].values
        y_bezirk = bezirk_data[selected_spalte].values
    
        # Modell anpassen
        model = LinearRegression()
        model.fit(X_bezirk, y_bezirk)
    
        # Vorhersagen für die nächsten 3 Jahre
        future_years = np.array([[2024], [2025], [2026]])
        predictions_bezirk = model.predict(future_years)
    
        # Vorhersagen runden und in Ganzzahlen umwandeln
        predictions_bezirk = np.round(predictions_bezirk).astype(int)
    
        # MAE und R² berechnen
        y_pred = model.predict(X_bezirk)
        mae = mean_absolute_error(y_bezirk, y_pred)
        r2 = r2_score(y_bezirk, y_pred)
    
        # Ergebnisse in einer gut formatierten Tabelle anzeigen
        prediction_results = pd.DataFrame({
            'Jahr': future_years.flatten(),
            selected_spalte + '_vorhersage': predictions_bezirk
        })
        
        st.markdown("<div class='centered-content'>", unsafe_allow_html=True)
        st.write(f"Vorhergesagte Werte für die nächsten 3 Jahre für {selected_bezirk} ({selected_spalte}):")
        st.table(prediction_results)
        st.markdown("</div>", unsafe_allow_html=True)
    
        # Interaktives Liniendiagramm mit plotly für den ausgewählten Bezirk
        fig = go.Figure()
    
        # Historische Daten hinzufügen
        fig.add_trace(go.Scatter(x=X_bezirk.flatten(), y=y_bezirk, mode='lines+markers', name='Historische Werte'))
    
        # Vorhersagen hinzufügen
        fig.add_trace(go.Scatter(x=future_years.flatten(), y=predictions_bezirk, mode='lines+markers', name='Vorhersage', line=dict(dash='dash')))
    
        fig.update_layout(
            title=f'{selected_spalte} in {selected_bezirk}',
            xaxis_title='Jahr',
            yaxis_title=selected_spalte,
            hovermode='x unified'
        )
    
        # Plot anzeigen in Streamlit
        st.markdown("<div class='centered-content'>", unsafe_allow_html=True)
        st.plotly_chart(fig)
        st.markdown("</div>", unsafe_allow_html=True)
    
        # MAE und R² anzeigen
        st.markdown("<div class='centered-content'>", unsafe_allow_html=True)
        st.write(f"Mean Absolute Error (MAE) für {selected_bezirk} ({selected_spalte}):", mae)
        st.write(f"R² für {selected_bezirk} ({selected_spalte}):", r2)
        st.markdown("</div>", unsafe_allow_html=True)
    
        # Option, die Ergebnisse als CSV herunterzuladen
        st.markdown("<div class='centered-content'>", unsafe_allow_html=True)
        csv = prediction_results.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Ergebnisse als CSV herunterladen",
            data=csv,
            file_name=f'vorhersage_{selected_spalte}_{selected_bezirk}.csv',
            mime='text/csv',
        )
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Liniendiagramm für alle Bezirke anzeigen
        st.markdown("<h2 style='text-align: center;'>Vorhersage für alle Bezirke (2024-2026)</h2>", unsafe_allow_html=True)
        fig_all = go.Figure()
        
        for bezirk in bezirk_list:
            bezirk_data = data[data['Bezeichnung_(Bezirksregion)'] == bezirk]
            X_bezirk = bezirk_data[['Jahr']].values
            y_bezirk = bezirk_data[selected_spalte].values
            
            model.fit(X_bezirk, y_bezirk)
            predictions_bezirk = model.predict(future_years)
            predictions_bezirk = np.round(predictions_bezirk).astype(int)
            
            # Vorhersagen für jeden Bezirk hinzufügen
            fig_all.add_trace(go.Scatter(x=future_years.flatten(), y=predictions_bezirk, mode='lines+markers', name=f'{bezirk} Vorhersage'))
        
        fig_all.update_layout(
            title=f'Vorhersagen für alle Bezirke ({selected_spalte})',
            xaxis_title='Jahr',
            yaxis_title='Vorhersage',
            hovermode='x unified'
        )
        
        st.markdown("<div class='centered-content'>", unsafe_allow_html=True)
        st.plotly_chart(fig_all)
        st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
