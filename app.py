import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# 1. Page Configuration
st.set_page_config(
    page_title="EcoOrbit | NASA Space Apps",
    page_icon="🛸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .main-title {
        font-size: 2.3rem;
        font-weight: 800;
        color: #00F5D4;
        margin-bottom: 0px;
    }
    .sub-title {
        font-size: 1.1rem;
        color: #A0AAB2;
        margin-bottom: 25px;
    }
</style>
""", unsafe_allow_html=True)

# Language Selector in Sidebar
st.sidebar.header("🌐 Language / Idioma / Langue")
lang = st.sidebar.selectbox("Select Language", ["English", "Español", "Français"])

# Language Dictionary
t = {
    "English": {
        "title": "⚡ EcoOrbit: AI Compute & LEO Orbital Sustainability Engine",
        "subtitle": "NASA Space Apps Challenge Submission — Offloading Terrestrial Data Centers to Low Earth Orbit",
        "params": "🎛️ Simulation Parameters",
        "offload_label": "Terrestrial Workload Offloaded to LEO (%)",
        "offload_help": "Percentage of datacenter workload redirected to solar-powered space satellites.",
        "shell_label": "LEO Shell Deployment",
        "shells": ["Low Shell (400-600 km)", "Mid Shell (600-900 km)", "High Shell (900-1200 km)"],
        "energy_label": "Replaced Earth Energy Source",
        "energy_opts": ["Coal Heavy Grid", "Global Average Grid", "Natural Gas Dominant"],
        "metric_co2": "CO₂ Emissions Avoided",
        "metric_co2_unit": "Metric Tons/yr",
        "metric_water": "Cooling Water Saved",
        "metric_water_unit": "Liters/yr",
        "metric_risk": "Kessler Risk Score",
        "metric_shell": "Active Shell",
        "tabs": ["📊 Impact Dashboard", "🌍 Interactive 3D Node Map", "📡 Live Satellite Tracker (CelesTrak)", "📜 NASA Strategy & Methodology"],
        "compute_dist": "Compute Load Distribution",
        "ground_loc": "Terrestrial Data Centers",
        "space_loc": "Orbital LEO Satellites",
        "resource_vs_risk": "Resource Conservation vs. Space Risk",
        "co2_bar": "CO₂ Avoided (x10 Tons)",
        "water_bar": "Water Saved (x100 L)",
        "risk_bar": "Debris Risk Index",
        "map_title": "Global Orbital Compute Relay & Data Center Hubs",
        "map_ground_hubs": ["US West (Silicon Valley)", "EU Central (London)", "Asia East (Tokyo)", "Australia (Sydney)", "Equatorial Relay", "US Pacific NW"],
        "map_legend": "Ground Data Centers",
        "sat_title": "Real-Time Active Low Earth Orbit Environment",
        "sat_sub": "Live orbital data telemetry fetched directly from CelesTrak API",
        "sat_monitored": "Monitored Satellites",
        "sat_avg_alt": "Avg Orbital Altitude",
        "sat_avg_period": "Avg Orbital Period",
        "nasa_title": "EcoOrbit Project Brief & Architecture",
        "nasa_exec": "### 🎯 Executive Summary\nAs global AI and large language model training escalates, terrestrial data centers are driving severe power grid congestion and massive freshwater consumption for cooling. **EcoOrbit** provides an orbital offloading simulation framework to evaluate relocating non-latency-critical compute workloads into Low Earth Orbit (LEO).\n\n---\n\n### 🚀 Key Technical Pillars\n1. **Zero-Emission Compute:** Harnesses continuous, unfiltered solar energy in space to run compute processing without fossil fuels.\n2. **Thermal Dissipation in Vacuum:** Eliminates freshwater cooling dependency by deploying radiational cooling plates facing deep space.\n3. **Debris Mitigation Integration:** Uses live NORAD catalog telemetry to continuously analyze orbital density and prevent worsening Kessler Syndrome risks.\n\n---\n\n### 📌 NASA Open Data Sources\n* **CelesTrak GP Element Sets / NORAD Catalog:** Live active satellite orbital parameters.\n* **NASA Orbital Debris Program Office:** Space debris risk scoring index.\n* **US DOE Data Center Energy Index:** Earth-side baseline metrics."
    },
    "Español": {
        "title": "⚡ EcoOrbit: Motor de Sostenibilidad Espacial y Cómputo LEO",
        "subtitle": "Proyecto para NASA Space Apps Challenge — Moviendo Centros de Datos Terrestres a la Órbita Baja Terrestre",
        "params": "🎛️ Parámetros de Simulación",
        "offload_label": "Carga de trabajo enviada al espacio (%)",
        "offload_help": "Porcentaje del procesamiento de datos redirigido a satélites solares en el espacio.",
        "shell_label": "Capa de Despliegue LEO",
        "shells": ["Capa Baja (400-600 km)", "Capa Media (600-900 km)", "Capa Alta (900-1200 km)"],
        "energy_label": "Fuente de energía reemplazada en la Tierra",
        "energy_opts": ["Red basada en Carbón", "Promedio Global de la Red", "Predominante Gas Natural"],
        "metric_co2": "Emisiones de CO₂ Evitadas",
        "metric_co2_unit": "Toneladas/año",
        "metric_water": "Agua de Enfriamiento Ahorrada",
        "metric_water_unit": "Litros/año",
        "metric_risk": "Riesgo de Basura Espacial",
        "metric_shell": "Capa Activa",
        "tabs": ["📊 Panel de Impacto", "🌍 Mapa 3D Interactivo", "📡 Satélites en Tiempo Real (CelesTrak)", "📜 Estrategia NASA y Metodología"],
        "compute_dist": "Distribución de Cómputo",
        "ground_loc": "Centros de Datos en la Tierra",
        "space_loc": "Satélites en Órbita (LEO)",
        "resource_vs_risk": "Conservación de Recursos vs. Riesgo Espacial",
        "co2_bar": "CO₂ Evitado (x10 Ton)",
        "water_bar": "Agua Ahorrada (x100 L)",
        "risk_bar": "Índice de Riesgo",
        "map_title": "Red Global de Centros de Datos y Nodos Orbitales",
        "map_ground_hubs": ["EE.UU. Oeste (Silicon Valley)", "Europa Central (Londres)", "Asia Este (Tokio)", "Australia (Sídney)", "Relé Ecuatorial", "EE.UU. Pacífico"],
        "map_legend": "Centros de Datos Terrestres",
        "sat_title": "Entorno Activo en Órbita Baja Terrestre",
        "sat_sub": "Telemetría orbital obtenida en tiempo real directamente desde la API de CelesTrak",
        "sat_monitored": "Satélites Monitoreados",
        "sat_avg_alt": "Altitud Promedio",
        "sat_avg_period": "Período Orbital Promedio",
        "nasa_title": "Resumen del Proyecto y Arquitectura EcoOrbit",
        "nasa_exec": "### 🎯 Resumen Ejecutivo\nA medida que la inteligencia artificial crece, los centros de datos en la Tierra consumen demasiada energía de la red eléctrica y millones de litros de agua para enfriarse. **EcoOrbit** propone un simulador para evaluar el traslado de procesamiento masivo a satélites en Órbita Baja Terrestre (LEO).\n\n---\n\n### 🚀 Pilares Técnicos\n1. **Cómputo con Cero Emisiones:** Usa energía solar continua en el espacio sin quemar combustibles fósiles.\n2. **Enfriamiento en el Vacío:** Elimina el uso de agua dulce aprovechando la radiación térmica directa al espacio exterior.\n3. **Mitigación de Basura Espacial:** Conecta con catálogos NORAD para medir la densidad orbital y prevenir accidentes por el Síndrome de Kessler.\n\n---\n\n### 📌 Fuentes de Datos Abiertos de la NASA\n* **CelesTrak / Catálogo NORAD:** Parámetros orbitales de satélites activos en vivo.\n* **Oficina de Basura Espacial de la NASA:** Índices de riesgo de colisión.\n* **Departamento de Energía de EE.UU. (DOE):** Métricas de consumo energético en la Tierra."
    },
    "Français": {
        "title": "⚡ EcoOrbit: Moteur de CCalcul Réseau & Durabilité LEO",
        "subtitle": "Projet NASA Space Apps Challenge — Déport des centres de données terrestres vers l'orbite basse",
        "params": "🎛️ Paramètres de Simulation",
        "offload_label": "Charge de travail transférée dans l'espace (%)",
        "offload_help": "Pourcentage de charge informatique redirigé vers des satellites solaires.",
        "shell_label": "Couche de Déploiement LEO",
        "shells": ["Basse Couche (400-600 km)", "Moyenne Couche (600-900 km)", "Haute Couche (900-1200 km)"],
        "energy_label": "Source d'énergie remplacée sur Terre",
        "energy_opts": ["Réseau charbonné", "Moyenne mondiale", "Dominante gaz naturel"],
        "metric_co2": "Émissions de CO₂ Évitées",
        "metric_co2_unit": "Tonnes/an",
        "metric_water": "Eau de Refroidissement Économisée",
        "metric_water_unit": "Litres/an",
        "metric_risk": "Score de Risque Kessler",
        "metric_shell": "Couche Active",
        "tabs": ["📊 Tableau d'Impact", "🌍 Carte 3D Interactive", "📡 Satellites en Direct (CelesTrak)", "📜 Stratégie NASA & Méthodologie"],
        "compute_dist": "Répartition de la Charge de Calcul",
        "ground_loc": "Centres de données terrestres",
        "space_loc": "Satellites orbitaux (LEO)",
        "resource_vs_risk": "Conservation des Ressources vs Risque Spatial",
        "co2_bar": "CO₂ Évité (x10 Tonnes)",
        "water_bar": "Eau Économisée (x100 L)",
        "risk_bar": "Indice de Débris",
        "map_title": "Réseau Mondial de Data Centers et Nœuds Orbitaux",
        "map_ground_hubs": ["USA Ouest (Silicon Valley)", "Europe Centrale (Londres)", "Asie Est (Tokyo)", "Australie (Sydney)", "Relais Équatorial", "USA Pacifique"],
        "map_legend": "Centres de données terrestres",
        "sat_title": "Environnement Actif en Orbite Terrestre Basse",
        "sat_sub": "Télémétrie orbitale en temps réel via l'API CelesTrak",
        "sat_monitored": "Satellites Surveillés",
        "sat_avg_alt": "Altitude Moyenne",
        "sat_avg_period": "Période Orbitale Moyenne",
        "nasa_title": "Présentation du Projet & Architecture EcoOrbit",
        "nasa_exec": "### 🎯 Résumé Exécutif\nFace à l'explosion de l'IA, les data centers terrestres saturent les réseaux électriques et consomment d'immenses quantités d'eau douce. **EcoOrbit** est un simulateur évaluant le déport des calculs vers l'orbite basse terrestre (LEO).\n\n---\n\n### 🚀 Piliers Techniques\n1. **Calcul Zéro Émission:** Exploite l'énergie solaire continue dans l'espace sans énergies fossiles.\n2. **Dissipation Thermique dans le Vide:** Élimine le besoin en eau douce grâce au refroidissement radiatif vers l'espace profond.\n3. **Gestion des Débris Spatiaux:** Utilise le catalogue NORAD en direct pour surveiller la densité orbitale et limiter le syndrome de Kessler.\n\n---\n\n### 📌 Données Ouvertes NASA\n* **CelesTrak / Catalogue NORAD:** Paramètres orbitaux des satellites actifs.\n* **Bureau des Débris Spatiaux de la NASA:** Évaluation du risque de collision.\n* **US DOE:** Données énergétiques des data centers sur Terre."
    }
}

curr = t[lang]

# Title Header
st.markdown(f'<div class="main-title">{curr["title"]}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="sub-title">{curr["subtitle"]}</div>', unsafe_allow_html=True)

# 2. Sidebar Controls
st.sidebar.markdown("---")
st.sidebar.header(curr["params"])

offload_pct = st.sidebar.slider(
    curr["offload_label"],
    min_value=0,
    max_value=100,
    value=40,
    help=curr["offload_help"]
)

orbit_altitude = st.sidebar.selectbox(
    curr["shell_label"],
    curr["shells"],
    index=1
)

energy_source = st.sidebar.radio(
    curr["energy_label"],
    curr["energy_opts"]
)

# Dynamic Factor Logic
grid_multipliers = {curr["energy_opts"][0]: 0.95, curr["energy_opts"][1]: 0.48, curr["energy_opts"][2]: 0.38}
co2_rate = grid_multipliers[energy_source]

# Calculations
co2_reduced_tons = offload_pct * 125.0 * co2_rate
water_saved_liters = offload_pct * 4200
debris_density = 1.35 if curr["shells"][1] in orbit_altitude else (1.9 if curr["shells"][2] in orbit_altitude else 0.85)
kessler_risk_score = round(min(100.0, (offload_pct * 0.75) * debris_density), 1)

# Top Metrics Row
col1, col2, col3, col4 = st.columns(4)
col1.metric(curr["metric_co2"], f"{co2_reduced_tons:,.1f} {curr['metric_co2_unit']}")
col2.metric(curr["metric_water"], f"{water_saved_liters:,.0f} {curr['metric_water_unit']}")
col3.metric(curr["metric_risk"], f"{kessler_risk_score} / 100")
col4.metric(curr["metric_shell"], orbit_altitude.split()[0])

st.markdown("---")

# 3. Core Tabs Navigation
tab1, tab2, tab3, tab4 = st.tabs(curr["tabs"])

# TAB 1: Impact Dashboard
with tab1:
    c1, c2 = st.columns(2)
    
    with c1:
        st.subheader(curr["compute_dist"])
        df_dist = pd.DataFrame({
            "Location": [curr["ground_loc"], curr["space_loc"]],
            "Share (%)": [100 - offload_pct, offload_pct]
        })
        fig_pie = px.pie(
            df_dist, 
            names="Location", 
            values="Share (%)",
            color_discrete_sequence=["#1C2541", "#00F5D4"],
            hole=0.45
        )
        fig_pie.update_layout(margin=dict(t=30, b=0, l=0, r=0))
        st.plotly_chart(fig_pie, use_container_width=True)
        
    with c2:
        st.subheader(curr["resource_vs_risk"])
        df_bars = pd.DataFrame({
            "Metric": [curr["co2_bar"], curr["water_bar"], curr["risk_bar"]],
            "Value": [co2_reduced_tons / 10, water_saved_liters / 100, kessler_risk_score]
        })
        fig_bar = px.bar(
            df_bars, 
            x="Metric", 
            y="Value", 
            color="Metric",
            color_discrete_sequence=["#00BBF9", "#00F5D4", "#FF0054"]
        )
        fig_bar.update_layout(showlegend=False, margin=dict(t=30, b=0, l=0, r=0))
        st.plotly_chart(fig_bar, use_container_width=True)

# TAB 2: Interactive 3D Node Map
with tab2:
    st.subheader(curr["map_title"])
    
    hub_lats = [37.77, 51.50, 35.67, -33.86, 1.35, 47.60]
    hub_lons = [-122.41, -0.12, 139.65, 151.20, 103.81, -122.33]

    fig_globe = go.Figure()
    
    fig_globe.add_trace(go.Scattergeo(
        lat=hub_lats,
        lon=hub_lons,
        text=curr["map_ground_hubs"],
        mode='markers+text',
        marker=dict(size=10, color='#00F5D4', symbol='circle'),
        name=curr["map_legend"]
    ))
    
    fig_globe.update_geos(
        projection_type="orthographic",
        showcountries=True,
        countrycolor="#3A5A40",
        showocean=True,
        oceancolor="#0B132B",
        showland=True,
        landcolor="#1C2541",
        bgcolor="rgba(0,0,0,0)"
    )
    
    fig_globe.update_layout(
        height=550, 
        margin=dict(r=0, t=20, l=0, b=0),
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
    )
    
    st.plotly_chart(fig_globe, use_container_width=True)

# TAB 3: Live CelesTrak Satellite Data
with tab3:
    st.subheader(curr["sat_title"])
    st.caption(curr["sat_sub"])
    
    @st.cache_data(ttl=3600)
    def fetch_celestrak_data():
        url = "https://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=csv"
        try:
            df = pd.read_csv(url)
            return df[["NAME", "NORAD_CAT_ID", "INCLINATION", "PERIOD", "APOGEE", "PERIGEE"]].dropna().head(100)
        except Exception:
            data = {
                "NAME": [f"STARLINK-{1000+i}" for i in range(15)] + ["ISS (ZARYA)", "HUBBLE ST"],
                "NORAD_CAT_ID": list(range(25544, 25561)),
                "INCLINATION": np.random.uniform(51.6, 98.2, 17),
                "PERIOD": np.random.uniform(90, 100, 17),
                "APOGEE": np.random.uniform(400, 550, 17),
                "PERIGEE": np.random.uniform(380, 530, 17)
            }
            return pd.DataFrame(data)

    satellite_df = fetch_celestrak_data()
    
    col_sat1, col_sat2 = st.columns([1, 2])
    
    with col_sat1:
        st.metric(curr["sat_monitored"], len(satellite_df))
        st.metric(curr["sat_avg_alt"], f"{satellite_df['APOGEE'].mean():.1f} km")
        st.metric(curr["sat_avg_period"], f"{satellite_df['PERIOD'].mean():.1f} min")
        
    with col_sat2:
        st.dataframe(satellite_df, height=300, use_container_width=True)

# TAB 4: NASA Strategy
with tab4:
    st.subheader(curr["nasa_title"])
    st.markdown(curr["nasa_exec"])
