import pandas as pd
import streamlit as st
import plotly.express as px

# Lectura del CSV (ruta relativa)
try:
    car_data = pd.read_csv("vehicles_us.csv")
except UnicodeDecodeError:
    # Fallback por si el CSV no está en utf-8
    car_data = pd.read_csv("vehicles_us.csv", encoding="latin-1")

# Encabezado
st.header("Anuncios de venta de coches — Dashboard Sprint 7")

# Vista previa rápida
with st.expander("Ver primeras filas"):
    st.write(car_data.head())
    st.write(f"Filas: {len(car_data):,} | Columnas: {car_data.shape[1]}")

# Botón para Histograma
hist_button = st.button("Construir histograma")

if hist_button:
    st.write("Creación de un histograma para la columna **odometer**")
    # Quitamos nulos de 'odometer' solo para el gráfico
    df_hist = car_data.dropna(subset=["odometer"])
    fig = px.histogram(df_hist, x="odometer", nbins=30)
    st.plotly_chart(fig, use_container_width=True)

# Botón para Dispersión 
scatter_button = st.button("Construir gráfico de dispersión")

if scatter_button:
    st.write("Creación de un gráfico de dispersión **price** vs **odometer**")
    # Quitamos nulos de columnas necesarias
    df_scatter = car_data.dropna(subset=["odometer", "price"])
    fig2 = px.scatter(df_scatter, x="odometer", y="price")
    st.plotly_chart(fig2, use_container_width=True)
