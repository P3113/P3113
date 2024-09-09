# -*- coding: utf-8 -*-
"""
Created on Mon Aug 26 13:15:27 2024

@author: P3113
"""
import streamlit as st

# Importieren Sie Ihre Module
import trends
import Prediction2024
import linReg
import mapp
import map

# Titel der Streamlit-Seite
st.markdown("<h1 style='text-align: center;'>PKS BERLIN</h1>", unsafe_allow_html=True)
st.write("")
st.write("")
st.write("")

pages = {
    "1. Trends"                  : trends,
    "2. Prediction 2024"         : Prediction2024,
    "3. Lineare Regression"      : linReg,
    "4. Map"                     : map,
    }

# Erstelle eine Seitenleiste für die Navigation im Projekt
st.sidebar.title("Navigation")
select = st.sidebar.radio("Gehe zu:", list(pages.keys()))

# Starte die ausgewählte Seite
pages[select].main()
