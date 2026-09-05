# 🦠 COVID-19 Global Dashboard

Dashboard interactivo para explorar la evolución de la pandemia COVID-19 a nivel mundial, construido con **Streamlit** y **Plotly**.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35%2B-FF4B4B?logo=streamlit)
![Plotly](https://img.shields.io/badge/Plotly-5.15%2B-3F4F75?logo=plotly)
![Datos](https://img.shields.io/badge/Datos-Our%20World%20in%20Data-blue)

---

## 📊 Características

- **Métricas globales**: casos confirmados, muertes y personas vacunadas en todo el mundo
- **Filtro por país y rango de fechas** desde la barra lateral
- **Evolución temporal** de nuevos casos y muertes diarias (gráfico de área)
- **Top 15 países** con más casos totales (gráfico de barras)
- **Avance de vacunación** por país (1.ª dosis vs. vacunación completa)
- **Mapa mundial** con casos por millón de habitantes (choropleth)

## 🗂️ Estructura del proyecto

```
02-covid-dashboard/
├── app.py               # Aplicación principal
├── requirements.txt     # Dependencias
├── data/                # Datos CSV (no incluidos en el repo, ver instalación)
└── README.md
```

## 🚀 Instalación y uso

### 1. Clonar el repositorio

```bash
git clone https://github.com/iKmiloo/02-covid-dashboard.git
cd 02-covid-dashboard
```

### 2. Crear entorno virtual e instalar dependencias

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
```

### 3. Obtener los datos

El dataset se descarga automáticamente desde internet la primera vez que ejecutas la app.

Si no tienes conexión, descárgalo manualmente:

👉 [owid-covid-data.csv](https://covid.ourworldindata.org/data/owid-covid-data.csv)

Guárdalo en `data/owid-covid-data.csv`.

### 4. Ejecutar la app

```bash
streamlit run app.py
```

Abre tu navegador en `http://localhost:8501`.

## 📦 Dependencias

| Paquete | Versión mínima |
|---------|---------------|
| streamlit | 1.35.0 |
| pandas | 1.5.0 |
| plotly | 5.15.0 |

## 📄 Fuente de datos

[Our World in Data — COVID-19 Dataset](https://ourworldindata.org/covid-deaths)

Licencia: [Creative Commons BY 4.0](https://creativecommons.org/licenses/by/4.0/)

---

Desarrollado por **Camilo Sanchez Vasquez** · [GitHub](https://github.com/iKmiloo)
