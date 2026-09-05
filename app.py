import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# ── Configuración de la página ──────────────────────────────────────────────
st.set_page_config(
    page_title="COVID-19 Dashboard",
    page_icon="🦠",
    layout="wide",
)

# ── Carga de datos ───────────────────────────────────────────────────────────
LOCAL_PATH = os.path.join(os.path.dirname(__file__), "data", "owid-covid-data.csv")
DATA_URL   = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv"

COLS = [
    "iso_code", "continent", "location", "date",
    "total_cases", "new_cases",
    "total_deaths", "new_deaths",
    "people_vaccinated", "people_fully_vaccinated",
    "total_cases_per_million", "total_deaths_per_million",
    "population",
]

@st.cache_data(ttl=60 * 60 * 12)   # refresca cada 12 horas
def load_data():
    if os.path.exists(LOCAL_PATH):
        source = LOCAL_PATH
    else:
        st.info("📡 Descargando datos desde internet...")
        source = DATA_URL
    df = pd.read_csv(source, usecols=COLS, parse_dates=["date"])
    df = df[~df["iso_code"].str.startswith("OWID", na=True)]
    df = df[df["continent"].notna()]
    return df

with st.spinner("⏳ Cargando datos..."):
    try:
        df = load_data()
    except Exception as e:
        st.error(
            "❌ **No se pudieron cargar los datos.**\n\n"
            "**Solución:** Descarga el archivo desde "
            "[este enlace](https://covid.ourworldindata.org/data/owid-covid-data.csv) "
            "y guárdalo en `data/owid-covid-data.csv` dentro del proyecto.\n\n"
            f"Error: `{e}`"
        )
        st.stop()

# ── Sidebar ──────────────────────────────────────────────────────────────────
st.sidebar.markdown(
    "<div style='text-align:center; font-size:64px; line-height:1;'>🦠</div>",
    unsafe_allow_html=True,
)
st.sidebar.title("🦠 COVID-19 Dashboard")
st.sidebar.markdown("**Fuente:** [Our World in Data](https://ourworldindata.org/covid-deaths)")
st.sidebar.divider()

paises = sorted(df["location"].unique())
pais_default = "Colombia"
pais = st.sidebar.selectbox(
    "🌎 Selecciona un país",
    paises,
    index=paises.index(pais_default) if pais_default in paises else 0,
)

fecha_min = df["date"].min().date()
fecha_max = df["date"].max().date()
_fechas = st.sidebar.date_input(
    "📅 Rango de fechas",
    value=(fecha_min, fecha_max),
    min_value=fecha_min,
    max_value=fecha_max,
)
if len(_fechas) == 2:
    fecha_inicio, fecha_fin = _fechas
else:
    # While the user is mid-selection only one date is returned; keep defaults
    fecha_inicio, fecha_fin = fecha_min, fecha_max

st.sidebar.divider()
st.sidebar.markdown(
    "Desarrollado por **Camilo Sanchez Vasquez**  \n"
    "[![GitHub](https://img.shields.io/badge/GitHub-iKmiloo-181717?logo=github)](https://github.com/iKmiloo)"
)

# ── Filtros ──────────────────────────────────────────────────────────────────
df_pais = df[
    (df["location"] == pais) &
    (df["date"] >= pd.Timestamp(fecha_inicio)) &
    (df["date"] <= pd.Timestamp(fecha_fin))
].copy()

df_global = (
    df.sort_values("date")
      .groupby("location", as_index=False)
      .last()          # última fila (con ffill implícito por groupby+last)
)

# ── Encabezado ───────────────────────────────────────────────────────────────
st.title("🦠 Dashboard Global de COVID-19")
st.caption(f"Datos actualizados al **{fecha_max.strftime('%d %b %Y')}** · Fuente: Our World in Data")
st.divider()

# ── KPIs globales ────────────────────────────────────────────────────────────
st.subheader("🌍 Métricas Globales (acumulado)")
total_casos   = df_global["total_cases"].sum()
total_muertes = df_global["total_deaths"].sum()
total_vacunas = df_global["people_fully_vaccinated"].sum()

k1, k2, k3 = st.columns(3)
k1.metric("😷 Casos Confirmados",   f"{total_casos:,.0f}")
k2.metric("💀 Muertes Registradas", f"{total_muertes:,.0f}")
k3.metric("💉 Personas Vacunadas",  f"{total_vacunas:,.0f}")
st.divider()

# ── KPIs del país seleccionado ───────────────────────────────────────────────
# Obtiene el último valor NO nulo de cada columna por separado,
# porque OWID dejó de actualizar vacunación antes que casos/muertes.
def last_valid(col):
    s = df_pais[col].dropna()
    return s.iloc[-1] if not s.empty else None

ultima_cases  = last_valid("total_cases")
ultima_deaths = last_valid("total_deaths")
ultima_vac    = last_valid("people_fully_vaccinated")
ultima_cpm    = last_valid("total_cases_per_million")
st.subheader(f"📌 {pais} — Resumen del período")

if not df_pais.empty:
    c1, c2, c3, c4 = st.columns(4)
    def fmt_int(val):
        return f"{int(val):,}" if val is not None else "N/D"

    c1.metric("Casos totales",        fmt_int(ultima_cases))
    c2.metric("Muertes totales",      fmt_int(ultima_deaths))
    c3.metric("Vacunados (completo)", fmt_int(ultima_vac))
    c4.metric("Casos por millón",     f"{ultima_cpm:,.0f}" if ultima_cpm is not None else "N/D")
else:
    st.warning("No hay datos disponibles para el país y período seleccionados.")
st.divider()

# ── Fila 1: Evolución de casos y muertes ────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.subheader(f"📈 Nuevos casos diarios — {pais}")
    if not df_pais.empty:
        fig = px.area(df_pais, x="date", y="new_cases",
                      labels={"date": "Fecha", "new_cases": "Nuevos casos"},
                      color_discrete_sequence=["#E63946"], template="plotly_white")
        fig.update_layout(margin=dict(t=10, b=10))
        st.plotly_chart(fig, width='stretch')

with col2:
    st.subheader(f"💀 Muertes diarias — {pais}")
    if not df_pais.empty:
        fig = px.area(df_pais, x="date", y="new_deaths",
                      labels={"date": "Fecha", "new_deaths": "Muertes diarias"},
                      color_discrete_sequence=["#343A40"], template="plotly_white")
        fig.update_layout(margin=dict(t=10, b=10))
        st.plotly_chart(fig, width='stretch')
st.divider()

# ── Fila 2: Top países + Vacunación ─────────────────────────────────────────
col3, col4 = st.columns(2)

with col3:
    st.subheader("🏆 Top 15 países por casos totales")
    top15 = (df_global[["location", "total_cases"]].dropna()
             .nlargest(15, "total_cases").sort_values("total_cases"))
    fig = px.bar(top15, x="total_cases", y="location", orientation="h",
                 labels={"total_cases": "Casos totales", "location": ""},
                 color="total_cases", color_continuous_scale="Reds",
                 template="plotly_white")
    fig.update_layout(coloraxis_showscale=False, margin=dict(t=10, b=10))
    st.plotly_chart(fig, width='stretch')

with col4:
    st.subheader(f"💉 Avance de vacunación — {pais}")
    df_vac = df_pais[["date", "people_vaccinated", "people_fully_vaccinated"]].dropna()
    if not df_vac.empty:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df_vac["date"], y=df_vac["people_vaccinated"],
                                 name="Al menos 1 dosis", fill="tozeroy",
                                 line=dict(color="#457B9D", width=1.5)))
        fig.add_trace(go.Scatter(x=df_vac["date"], y=df_vac["people_fully_vaccinated"],
                                 name="Vacunación completa", fill="tozeroy",
                                 line=dict(color="#1D3557", width=1.5)))
        fig.update_layout(template="plotly_white",
                          legend=dict(orientation="h", yanchor="bottom", y=1.02),
                          margin=dict(t=10, b=10),
                          xaxis_title="Fecha", yaxis_title="Personas")
        st.plotly_chart(fig, width='stretch')
    else:
        st.info("Sin datos de vacunación para este país.")
st.divider()

# ── Mapa mundial ─────────────────────────────────────────────────────────────
st.subheader("🗺️ Mapa Mundial — Casos por millón de habitantes")
df_mapa = df_global[["iso_code", "location", "total_cases_per_million",
                      "total_cases", "total_deaths"]].dropna()
fig = px.choropleth(df_mapa, locations="iso_code", color="total_cases_per_million",
                    hover_name="location",
                    hover_data={"total_cases": ":,.0f", "total_deaths": ":,.0f",
                                "total_cases_per_million": ":,.0f", "iso_code": False},
                    color_continuous_scale="YlOrRd",
                    labels={"total_cases_per_million": "Casos/millón",
                            "total_cases": "Casos totales",
                            "total_deaths": "Muertes totales"},
                    template="plotly_white")
fig.update_layout(margin=dict(t=0, b=0, l=0, r=0),
                  coloraxis_colorbar=dict(title="Casos/millón"),
                  geo=dict(showframe=False, showcoastlines=True))
st.plotly_chart(fig, width='stretch')

st.caption("🔗 Datos: [Our World in Data](https://ourworldindata.org/covid-deaths) · Proyecto de portafolio — Camilo Sanchez Vasquez")