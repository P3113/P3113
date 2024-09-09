import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.preprocessing import StandardScaler
import plotly.graph_objects as go

def main():
    st.title('Prediction 2024')

    file_path = 'Bezirke 14-23 - Rohdaten.csv'
    data = pd.read_csv(file_path)
    
    if data is not None:
        bezirk_list = data['Bezeichnung_(Bezirksregion)'].unique()
        selected_bezirk = st.selectbox('Wähle einen Bezirk aus:', bezirk_list)
    
        spalten_list = [col for col in data.columns if col not in ['Bezeichnung_(Bezirksregion)', 'Jahr']]
        selected_spalte = st.selectbox('Wähle eine Spalte aus:', spalten_list)
    
        bezirk_data = data[data['Bezeichnung_(Bezirksregion)'] == selected_bezirk]
        X_bezirk = bezirk_data[['Jahr']].values
        y_bezirk = bezirk_data[selected_spalte].values
    
        # Features skalieren
        scaler = StandardScaler()
        X_bezirk_scaled = scaler.fit_transform(X_bezirk)
    
        # Modellwahl
        model_choice = st.selectbox('Wähle ein Modell:', ['KNN', 'SVM', 'Linear Regression', 'Random Forest'])

        if model_choice == 'KNN':
            model = KNeighborsRegressor(n_neighbors=5)
        elif model_choice == 'SVM':
            model = SVR(kernel='rbf', C=1.0, epsilon=0.1)
        elif model_choice == 'Linear Regression':
            model = LinearRegression()
        elif model_choice == 'Random Forest':
            model = RandomForestRegressor(n_estimators=100, random_state=42)
    
        # Modell anpassen
        model.fit(X_bezirk_scaled, y_bezirk)
    
        # Vorhersage für das Jahr 2024
        future_year = np.array([[2024]])
        future_year_scaled = scaler.transform(future_year)
        prediction_2024 = model.predict(future_year_scaled)
    
        # Ergebnis auf die nächste Ganzzahl runden
        prediction_2024 = np.round(prediction_2024).astype(int)
    
        y_pred = model.predict(X_bezirk_scaled)
        mae = mean_absolute_error(y_bezirk, y_pred)
        r2 = r2_score(y_bezirk, y_pred)
    
        prediction_results = pd.DataFrame({
            'Jahr': future_year.flatten(),
            selected_spalte + '_vorhersage': prediction_2024
        })
    
        st.write(f"Vorhergesagter Wert für das Jahr 2024 für {selected_bezirk} ({selected_spalte}):")
        st.table(prediction_results)
    
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=X_bezirk.flatten(), y=y_bezirk, mode='lines+markers', name='Historische Werte'))
        fig.add_trace(go.Scatter(x=future_year.flatten(), y=prediction_2024, mode='lines+markers', name=f'Vorhersage 2024 ({model_choice})', line=dict(dash='dash')))
    
        fig.update_layout(
            title=f'{selected_spalte} in {selected_bezirk} mit {model_choice}',
            xaxis_title='Jahr',
            yaxis_title=selected_spalte,
            hovermode='x unified'
        )
    
        st.plotly_chart(fig)
        st.write(f"Mean Absolute Error (MAE) für {selected_bezirk} ({selected_spalte}) mit {model_choice}:", mae)
        st.write(f"R² für {selected_bezirk} ({selected_spalte}) mit {model_choice}:", r2)
    
        csv = prediction_results.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Ergebnis als CSV herunterladen",
            data=csv,
            file_name=f'vorhersage_2024_{selected_spalte}_{selected_bezirk}_{model_choice}.csv',
            mime='text/csv',
        )

if __name__ == "__main__":
    main()
