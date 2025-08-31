import pandas as pd
import streamlit as st
import plotly.express as px

df = pd.read_csv("vehicles_us.csv")

# leer los datos
car_data = pd.read_csv("vehicles_us.csv")

st.header('Gráficas de vehiculos')
import pandas as pd
import streamlit as st
import plotly.express as px
from pathlib import Path

# ---------- Configuración global ----------
st.set_page_config(page_title="Car Listings Dashboard", layout="wide")

# ---------- Utilidades ----------
@st.cache_data(show_spinner="Cargando datos...")
def load_csv(path_like: str) -> pd.DataFrame:
    """Carga robusta: intenta utf-8 y latin-1; usa Path para compatibilidad Win/WSL."""
    p = Path(path_like)
    if not p.exists():
        return pd.DataFrame()
    try:
        return pd.read_csv(p)
    except UnicodeDecodeError:
        return pd.read_csv(p, encoding="latin-1")

def get_numeric_cols(df: pd.DataFrame) -> list[str]:
    return [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]

# ---------- Título / Descripción ----------
st.header("Anuncios de venta de coches — Dashboard Sprint 7")
st.caption("Explora rápidamente el dataset: histograma y dispersión con opciones configurables.")

# ---------- Entrada de datos ----------
with st.sidebar:
    st.subheader("Datos")
    csv_choice = st.radio(
        "Fuente de datos",
        ["Archivo local en el repo (vehicles_us.csv)", "Subir CSV"],
        index=0,
    )

    if csv_choice == "Subir CSV":
        uploaded = st.file_uploader("Sube un CSV", type=["csv"])
        if uploaded is not None:
            df = pd.read_csv(uploaded)
        else:
            df = pd.DataFrame()
    else:
        # Ruta relativa para que funcione local y en Render
        df = load_csv("vehicles_us.csv")

    # Persistimos el df en Session State para evitar recomputes por interacción
    if not df.empty:
        st.session_state["df"] = df

# Si no hay datos válidos, detenemos la app con un mensaje claro
if "df" not in st.session_state or st.session_state["df"].empty:
    st.info("🔹 Coloca `vehicles_us.csv` en la misma carpeta que `app.py` **o** sube un CSV desde la barra lateral.")
    st.stop()

df = st.session_state["df"]

# ---------- Vista previa ----------
with st.expander("👀 Vista previa de datos"):
    st.write(df.head(10))
    st.write(f"Filas: {len(df):,} | Columnas: {df.shape[1]}")

# ---------- Controles (sidebar) ----------
with st.sidebar:
    st.subheader("Controles de visualización")
    num_cols = get_numeric_cols(df)
    if not num_cols:
        st.warning("No se detectaron columnas numéricas en el dataset.")
    build_hist = st.checkbox("Mostrar histograma", value=True)
    build_scatter = st.checkbox("Mostrar dispersión", value=True)

# ---------- Histograma ----------
if build_hist and num_cols:
    st.subheader("Histograma")
    col_hist_1, col_hist_2, col_hist_3 = st.columns([2, 1, 1])
    with col_hist_1:
        x_hist = st.selectbox(
            "Columna (X)",
            options=num_cols,
            index=num_cols.index("odometer") if "odometer" in num_cols else 0,
            key="hist_x",
        )
    with col_hist_2:
        bins = st.slider("Bins", min_value=5, max_value=100, value=30, step=5)
    with col_hist_3:
        log_x = st.checkbox("Escala log X", value=False)

    fig_h = px.histogram(df, x=x_hist, nbins=bins)
    if log_x:
        fig_h.update_xaxes(type="log")
    st.plotly_chart(fig_h, use_container_width=True)

# ---------- Dispersión ----------
if build_scatter and len(num_cols) >= 2:
    st.subheader("Gráfico de dispersión")
    col_sc_1, col_sc_2, col_sc_3, col_sc_4 = st.columns([2, 2, 2, 2])

    default_x = "odometer" if "odometer" in num_cols else num_cols[0]
    default_y = "price" if "price" in num_cols else (num_cols[1] if len(num_cols) > 1 else num_cols[0])

    with col_sc_1:
        x_sc = st.selectbox("X", options=num_cols, index=num_cols.index(default_x) if default_x in num_cols else 0)
    with col_sc_2:
        y_sc = st.selectbox("Y", options=num_cols, index=num_cols.index(default_y) if default_y in num_cols else 0)
    with col_sc_3:
        color_opt = st.selectbox("Color (opcional)", options=["(ninguno)"] + list(df.columns))
    with col_sc_4:
        sample_n = st.slider("Muestreo (máx. filas)", 100, min(10000, len(df)), min(2000, len(df)), step=100)

    # Muestreo para mejorar rendimiento con datasets grandes
    df_plot = df.sample(n=min(sample_n, len(df)), random_state=42) if len(df) > sample_n else df

    color_kw = {} if color_opt == "(ninguno)" else {"color": color_opt}
    fig_s = px.scatter(df_plot, x=x_sc, y=y_sc, **color_kw)
    st.plotly_chart(fig_s, use_container_width=True)

st.caption("Hecho con Streamlit + Plotly Express + Pandas · Sprint 7")