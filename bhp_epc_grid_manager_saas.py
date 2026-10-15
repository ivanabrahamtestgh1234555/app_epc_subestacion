import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# -----------------------------------------------------------------------------
# PAGE CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="BHP EPC-Grid Manager SaaS | Proyecto ENC-3430",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #4B5563;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background-color: #F3F4F6;
        border-left: 5px solid #2563EB;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .stMetric label {
        font-weight: 600 !important;
        color: #374151 !important;
    }
    .soil-badge-s1 { background-color: #EF4444; color: white; padding: 3px 8px; border-radius: 4px; font-weight: bold; }
    .soil-badge-s2 { background-color: #F59E0B; color: white; padding: 3px 8px; border-radius: 4px; font-weight: bold; }
    .soil-badge-s3 { background-color: #10B981; color: white; padding: 3px 8px; border-radius: 4px; font-weight: bold; }
    .soil-badge-s4 { background-color: #3B82F6; color: white; padding: 3px 8px; border-radius: 4px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# DATASET INITIALIZATION
# -----------------------------------------------------------------------------
@st.cache_data
def load_project_data():
    # 1. Summary CAPEX Data
    summary_df = pd.DataFrame([
        {"Area": "S/E EGP 220/33 kV (GIS)", "Direct_Cost_USD": 35158330, "Concrete_m3": 1090.8, "Steel_kg": 263722, "Excavation_m3": 7638.7},
        {"Area": "S/E Monte Mina 220 kV (AIS)", "Direct_Cost_USD": 8845200, "Concrete_m3": 450.0, "Steel_kg": 5270, "Excavation_m3": 2100.0},
        {"Area": "Línea Transmisión 2x220 kV", "Direct_Cost_USD": 16248350, "Concrete_m3": 1206.5, "Steel_kg": 1054948, "Excavation_m3": 6622.7}
    ])
    
    # 2. Detailed MTO / Cubicaciones
    mto_data = [
        # SE EGP
        {"Area": "SE EGP 220/33 kV", "Disciplina": "Civil / Geotecnia", "Item": "Excavación Suelo Tipo 1 (Roca Sana)", "Unidad": "m³", "Cantidad": 1145.8, "Unit_Cost_USD": 45.0, "Total_USD": 51561.0, "Status": "Aprobado Class 3"},
        {"Area": "SE EGP 220/33 kV", "Disciplina": "Civil / Geotecnia", "Item": "Excavación Suelo Tipo 2 (Roca Agrietada/H-3)", "Unidad": "m³", "Cantidad": 2673.5, "Unit_Cost_USD": 32.0, "Total_USD": 85552.0, "Status": "Aprobado Class 3"},
        {"Area": "SE EGP 220/33 kV", "Disciplina": "Civil / Geotecnia", "Item": "Excavación Suelo Tipo 3 (Grava Densa/H-1)", "Unidad": "m³", "Cantidad": 2673.5, "Unit_Cost_USD": 22.0, "Total_USD": 58817.0, "Status": "Aprobado Class 3"},
        {"Area": "SE EGP 220/33 kV", "Disciplina": "Civil / Geotecnia", "Item": "Excavación Suelo Tipo 4 (Suelo Fino/H-2)", "Unidad": "m³", "Cantidad": 1145.8, "Unit_Cost_USD": 18.0, "Total_USD": 20624.0, "Status": "Aprobado Class 3"},
        {"Area": "SE EGP 220/33 kV", "Disciplina": "Estructural", "Item": "Hormigón Estructural G35 Pedestales/Fundaciones", "Unidad": "m³", "Cantidad": 286.0, "Unit_Cost_USD": 420.0, "Total_USD": 120120.0, "Status": "Aprobado Class 3"},
        {"Area": "SE EGP 220/33 kV", "Disciplina": "Estructural", "Item": "Hormigón Estructural G35 Muros Cortafuego", "Unidad": "m³", "Cantidad": 512.8, "Unit_Cost_USD": 480.0, "Total_USD": 246144.0, "Status": "Aprobado Class 3"},
        {"Area": "SE EGP 220/33 kV", "Disciplina": "Estructural", "Item": "Armadura Acero A630-420H", "Unidad": "kg", "Cantidad": 252183.0, "Unit_Cost_USD": 2.60, "Total_USD": 655675.8, "Status": "Aprobado Class 3"},
        {"Area": "SE EGP 220/33 kV", "Disciplina": "Electromecánica", "Item": "Switchgear GIS 245 kV (Suministro/Montaje)", "Unidad": "Gl", "Cantidad": 1.0, "Unit_Cost_USD": 14500000.0, "Total_USD": 14500000.0, "Status": "Long Lead / Precommitment"},
        {"Area": "SE EGP 220/33 kV", "Disciplina": "Electromecánica", "Item": "Transformador Poder 220/33 kV 125 MVA", "Unidad": "c/u", "Cantidad": 3.0, "Unit_Cost_USD": 3800000.0, "Total_USD": 11400000.0, "Status": "Long Lead / Precommitment"},
        {"Area": "SE EGP 220/33 kV", "Disciplina": "Electromecánica", "Item": "Ducto de Barras GIL 220 kV", "Unidad": "Gl", "Cantidad": 1.0, "Unit_Cost_USD": 3200000.0, "Total_USD": 3200000.0, "Status": "Licitación"},
        
        # SE Monte Mina
        {"Area": "SE Monte Mina 220 kV", "Disciplina": "Electromecánica", "Item": "Interruptor Tanque Muerto SF6 220 kV 3150A", "Unidad": "c/u", "Cantidad": 3.0, "Unit_Cost_USD": 220000.0, "Total_USD": 660000.0, "Status": "Aprobado Class 3"},
        {"Area": "SE Monte Mina 220 kV", "Disciplina": "Electromecánica", "Item": "Transformador Potencial Capacitivo TPC 220 kV", "Unidad": "c/u", "Cantidad": 10.0, "Unit_Cost_USD": 42000.0, "Total_USD": 420000.0, "Status": "Aprobado Class 3"},
        {"Area": "SE Monte Mina 220 kV", "Disciplina": "Electromecánica", "Item": "Cable Aislado XLPE 220 kV 3000 mm²", "Unidad": "m", "Cantidad": 1800.0, "Unit_Cost_USD": 450.0, "Total_USD": 810000.0, "Status": "Long Lead"},
        {"Area": "SE Monte Mina 220 kV", "Disciplina": "Electromecánica", "Item": "Mufas Transición Aire/Cable 220 kV", "Unidad": "c/u", "Cantidad": 12.0, "Unit_Cost_USD": 35000.0, "Total_USD": 420000.0, "Status": "Long Lead"},
        {"Area": "SE Monte Mina 220 kV", "Disciplina": "Civil / Geotecnia", "Item": "Excavación Patio AIS y Patios Mufas", "Unidad": "m³", "Cantidad": 2100.0, "Unit_Cost_USD": 25.0, "Total_USD": 52500.0, "Status": "Aprobado Class 3"},
        
        # Linea 220 kV
        {"Area": "Línea Transmisión 220 kV", "Disciplina": "Estructural", "Item": "Torres Suspensión 22AD.1M3 (84 Torres Total)", "Unidad": "kg", "Cantidad": 662580.0, "Unit_Cost_USD": 4.20, "Total_USD": 2782836.0, "Status": "Aprobado Class 3"},
        {"Area": "Línea Transmisión 220 kV", "Disciplina": "Estructural", "Item": "Torres Anclaje/Remate 22CD/22DD (18 Torres)", "Unidad": "kg", "Cantidad": 372300.0, "Unit_Cost_USD": 4.50, "Total_USD": 1675350.0, "Status": "Aprobado Class 3"},
        {"Area": "Línea Transmisión 220 kV", "Disciplina": "Civil / Geotecnia", "Item": "Excavaciones Obras Civiles LAT (S1 a S4)", "Unidad": "m³", "Cantidad": 6622.7, "Unit_Cost_USD": 28.5, "Total_USD": 188746.95, "Status": "Aprobado Class 3"},
        {"Area": "Línea Transmisión 220 kV", "Disciplina": "Civil / Geotecnia", "Item": "Hormigón Estructural G35 Fundaciones LAT", "Unidad": "m³", "Cantidad": 1206.5, "Unit_Cost_USD": 420.0, "Total_USD": 506730.0, "Status": "Aprobado Class 3"},
        {"Area": "Línea Transmisión 220 kV", "Disciplina": "Electromecánica", "Item": "Conductor AAAC Flint 740.8 MCM (25.7 km)", "Unidad": "m", "Cantidad": 312000.0, "Unit_Cost_USD": 14.50, "Total_USD": 4524000.0, "Status": "Aprobado Class 3"},
        {"Area": "Línea Transmisión 220 kV", "Disciplina": "Electromecánica", "Item": "Cable Guardia OPGW 24 Fibras Ópticas", "Unidad": "m", "Cantidad": 27000.0, "Unit_Cost_USD": 8.50, "Total_USD": 229500.0, "Status": "Aprobado Class 3"},
        {"Area": "Línea Transmisión 220 kV", "Disciplina": "Electromecánica", "Item": "Faenas de Tendido, Regulado y Flechado", "Unidad": "km", "Cantidad": 25.7, "Unit_Cost_USD": 42000.0, "Total_USD": 1079400.0, "Status": "Aprobado Class 3"}
    ]
    mto_df = pd.DataFrame(mto_data)
    
    # 3. Geotechnical Soil Data (ETG-A.0.10)
    soil_df = pd.DataFrame([
        {"Tipo_Suelo": "Suelo Tipo 1", "Nombre": "Roca Sana / Densa", "Desc": "Roca sana o moderadamente agrietada. Requiere explosivo/martillo neumático.", "Fundacion": "Cáncamos Anclados en Roca", "Vol_EGP_m3": 1145.8, "Vol_LAT_m3": 215.6, "Total_Vol_m3": 1361.4, "Unit_Cost_USD": 45.0},
        {"Tipo_Suelo": "Suelo Tipo 2", "Nombre": "Roca Agrietada / Grava Densa", "Desc": "Roca agrietada / Grava cementada. Excavación con martillo neumático.", "Fundacion": "Bloque de Hormigón en Masa", "Vol_EGP_m3": 2673.5, "Vol_LAT_m3": 645.6, "Total_Vol_m3": 3319.1, "Unit_Cost_USD": 32.0},
        {"Tipo_Suelo": "Suelo Tipo 3", "Nombre": "Grava Limpia Densa", "Desc": "Grava limpia compacidad media/alta con presencia de bolones.", "Fundacion": "Zapata Troncopiramidal + Pedestal", "Vol_EGP_m3": 2673.5, "Vol_LAT_m3": 3402.7, "Total_Vol_m3": 6076.2, "Unit_Cost_USD": 22.0},
        {"Tipo_Suelo": "Suelo Tipo 4", "Nombre": "Suelo Fino / Arena-Limo", "Desc": "Rocas descompuestas, arenas/limos de consistencia media.", "Fundacion": "Zapata Escalonada / Rectangular", "Vol_EGP_m3": 1145.8, "Vol_LAT_m3": 2358.8, "Total_Vol_m3": 3504.6, "Unit_Cost_USD": 18.0}
    ])
    
    # 4. Long Lead Supplies Tracking
    supplies_df = pd.DataFrame([
        {"Equipo": "Switchgear GIS 245 kV", "Proveedor": "Hitachi / ABB", "Lead_Time_Meses": 14, "Avance_Ingenieria": 95, "Estado_FAT": "Aprobado", "Arribo_Mina": "2027-02-15"},
        {"Equipo": "Transformadores 125 MVA (3 c/u)", "Proveedor": "Siemens Energy", "Lead_Time_Meses": 12, "Avance_Ingenieria": 90, "Estado_FAT": "En Proceso", "Arribo_Mina": "2026-11-30"},
        {"Equipo": "Cable XLPE 220 kV 3000 mm²", "Proveedor": "Prysmian Group", "Lead_Time_Meses": 8, "Avance_Ingenieria": 100, "Estado_FAT": "Aprobado", "Arribo_Mina": "2026-09-10"},
        {"Equipo": "Torres Anclaje 22DD.2M (12 c/u)", "Proveedor": "Metalúrgica SAE", "Lead_Time_Meses": 6, "Avance_Ingenieria": 100, "Estado_FAT": "Aprobado", "Arribo_Mina": "2026-08-20"},
        {"Equipo": "Cable Guardia OPGW 24FO", "Proveedor": "AFL Telecommunications", "Lead_Time_Meses": 5, "Avance_Ingenieria": 100, "Estado_FAT": "Aprobado", "Arribo_Mina": "2026-07-15"}
    ])

    return summary_df, mto_df, soil_df, supplies_df

summary_df, mto_df, soil_df, supplies_df = load_project_data()

# -----------------------------------------------------------------------------
# SIDEBAR NAVIGATION & CONTROLS
# -----------------------------------------------------------------------------
st.sidebar.markdown("## BHP EPC-Grid Manager")
st.sidebar.markdown("**Proyecto Escondida Concentrator (ENC-3430)**")
st.sidebar.markdown("---")

module = st.sidebar.radio(
    "Navegación de Módulos:",
    [
        "📊 Dashboard Principal & KPIs",
        "📦 Control de Cubicaciones y MTO",
        "🪨 Geotecnia y Suelos (ETG-A.0.10)",
        "💰 Simulador Financiero CAPEX",
        "🚚 Suministros Críticos (Long Lead)",
        "📤 Exportación de Informes"
    ]
)

st.sidebar.markdown("---")
st.sidebar.subheader("Filtros Globales de Vista")
selected_area = st.sidebar.multiselect(
    "Filtrar por Área:",
    options=mto_df["Area"].unique(),
    default=mto_df["Area"].unique()
)

# Filter dataframe by sidebar selection
filtered_mto = mto_df[mto_df["Area"].isin(selected_area)]

# -----------------------------------------------------------------------------
# MODULE 1: DASHBOARD PRINCIPAL & KPIS
# -----------------------------------------------------------------------------
if module == "📊 Dashboard Principal & KPIs":
    st.markdown('<div class="main-header">Resumen Ejecutivo de Gestión EPC</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Monitoreo Integrado de Cubicaciones, Materiales y CAPEX para Subestaciones y Línea de Transmisión</div>', unsafe_allow_html=True)
    
    # Top KPI Metrics
    c1, c2, c3, c4, c5 = st.columns(5)
    
    total_capex = summary_df["Direct_Cost_USD"].sum()
    total_excavation = summary_df["Excavation_m3"].sum()
    total_concrete = summary_df["Concrete_m3"].sum()
    total_steel = summary_df["Steel_kg"].sum()
    
    with c1:
        st.metric("CAPEX Directo Total", f"${total_capex:,.0f} USD", delta="+2.5% vs Base")
    with c2:
        st.metric("Vol. Excavación Total", f"{total_excavation:,.1f} m³", delta="ETG-A.0.10")
    with c3:
        st.metric("Hormigón Estructural", f"{total_concrete:,.1f} m³", delta="G35 / G10")
    with c4:
        st.metric("Estructuras y Acero", f"{total_steel:,.0f} kg", delta="84 Torres LAT")
    with c5:
        st.metric("Avance Físico Global", "38.5%", delta="+1.2% S-Curve")

    st.markdown("---")
    
    # Charts Row 1
    col_left, col_right = st.columns([6, 4])
    
    with col_left:
        st.subheader("Distribución de Costo Directo por Área de Proyecto (USD)")
        fig_capex = px.bar(
            summary_df,
            x="Area",
            y="Direct_Cost_USD",
            text_auto=".2s",
            color="Area",
            color_discrete_sequence=["#1E3A8A", "#2563EB", "#60A5FA"],
            labels={"Direct_Cost_USD": "Costo Directo (USD)", "Area": "Instalación"}
        )
        fig_capex.update_layout(showlegend=False, height=380, margin=dict(l=20, r=20, t=30, b=20))
        st.plotly_chart(fig_capex, use_container_width=True)

    with col_right:
        st.subheader("Volumen de Excavación por Tipo de Suelo")
        fig_soil = px.pie(
            soil_df,
            values="Total_Vol_m3",
            names="Tipo_Suelo",
            color="Tipo_Suelo",
            color_discrete_map={
                "Suelo Tipo 1": "#EF4444",
                "Suelo Tipo 2": "#F59E0B",
                "Suelo Tipo 3": "#10B981",
                "Suelo Tipo 4": "#3B82F6"
            },
            hole=0.4
        )
        fig_soil.update_layout(height=380, margin=dict(l=20, r=20, t=30, b=20))
        st.plotly_chart(fig_soil, use_container_width=True)

    # Charts Row 2
    st.subheader("Desglose de Costos por Disciplina Técnica")
    disc_summary = filtered_mto.groupby("Disciplina")["Total_USD"].sum().reset_index()
    fig_disc = px.treemap(
        filtered_mto,
        path=["Area", "Disciplina", "Item"],
        values="Total_USD",
        color="Total_USD",
        color_continuous_scale="Viridis"
    )
    fig_disc.update_layout(height=450, margin=dict(l=10, r=10, t=30, b=10))
    st.plotly_chart(fig_disc, use_container_width=True)

# -----------------------------------------------------------------------------
# MODULE 2: CONTROL DE CUBICACIONES Y MTO
# -----------------------------------------------------------------------------
elif module == "📦 Control de Cubicaciones y MTO":
    st.markdown('<div class="main-header">Listado Maestro de Cubicaciones (MTO / BOM)</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Búsqueda, Filtrado Dinámico y Control de Suministros por Instalación y Disciplina</div>', unsafe_allow_html=True)
    
    f1, f2, f3 = st.columns([4, 4, 4])
    with f1:
        disc_filter = st.multiselect("Disciplina:", options=mto_df["Disciplina"].unique(), default=mto_df["Disciplina"].unique())
    with f2:
        status_filter = st.multiselect("Estado de Aprobación:", options=mto_df["Status"].unique(), default=mto_df["Status"].unique())
    with f3:
        search_term = st.text_input("🔍 Buscar Ítem / Descripción:", "")

    # Apply filters
    view_df = filtered_mto[
        (filtered_mto["Disciplina"].isin(disc_filter)) &
        (filtered_mto["Status"].isin(status_filter))
    ]
    if search_term:
        view_df = view_df[view_df["Item"].str.contains(search_term, case=False, na=False)]

    st.markdown(f"**Mostrando {len(view_df)} registros encontrados:**")
    
    # Editable / Interactive Data Table
    st.dataframe(
        view_df.style.format({
            "Cantidad": "{:,.1f}",
            "Unit_Cost_USD": "${:,.2f}",
            "Total_USD": "${:,.2f}"
        }),
        use_container_width=True,
        height=400
    )
    
    # Subtotal Summary
    subtotal_cost = view_df["Total_USD"].sum()
    st.info(f"💡 **Subtotal Costo Directo de Selección:** ${subtotal_cost:,.2f} USD")

# -----------------------------------------------------------------------------
# MODULE 3: GEOTECNIA Y SUELOS (ETG-A.0.10)
# -----------------------------------------------------------------------------
elif module == "🪨 Geotecnia y Suelos (ETG-A.0.10)":
    st.markdown('<div class="main-header">Módulo Geotécnico y Clasificación de Suelos</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Criterios de Excavación y Tipología de Fundaciones según Especificación ETG-A.0.10</div>', unsafe_allow_html=True)
    
    # Soil detail cards
    cols = st.columns(4)
    for idx, row in soil_df.iterrows():
        with cols[idx]:
            st.markdown(f"### {row['Tipo_Suelo']}")
            st.markdown(f"**{row['Nombre']}**")
            st.write(row['Desc'])
            st.markdown(f"**Fundación:** {row['Fundacion']}")
            st.metric("Volumen Total", f"{row['Total_Vol_m3']:,.1f} m³")
            st.metric("P.U. Excavación", f"${row['Unit_Cost_USD']:.0f} USD/m³")

    st.markdown("---")
    st.subheader("🧮 Calculadora de Excavaciones y Hormigón para Fundaciones")
    
    calc_col1, calc_col2 = st.columns([5, 5])
    with calc_col1:
        st.markdown("#### Parámetros de Entrada de Plataforma / Obras Civil")
        calc_area = st.selectbox("Seleccionar Área de Proyecto:", ["S/E EGP 220/33 kV", "Línea de Transmisión 220 kV"])
        area_sqm = st.number_input("Superficie Afecta a Fundación (m²):", value=1500.0, step=100.0)
        depth_m = st.number_input("Profundidad Media de Sello (m):", value=2.2, step=0.1)
        
        st.markdown("**Distribución del Perfil de Suelo (debe sumar 100%):**")
        p_s1 = st.slider("% Suelo Tipo 1 (Roca Sana):", 0, 100, 15)
        p_s2 = st.slider("% Suelo Tipo 2 (Roca Agrietada):", 0, 100, 35)
        p_s3 = st.slider("% Suelo Tipo 3 (Grava Densa):", 0, 100, 35)
        p_s4 = st.slider("% Suelo Tipo 4 (Suelo Fino):", 0, 100, 15)

    with calc_col2:
        st.markdown("#### Resultados Estimados de Cubicación")
        total_calc_vol = area_sqm * depth_m
        
        v_s1 = total_calc_vol * (p_s1 / 100.0)
        v_s2 = total_calc_vol * (p_s2 / 100.0)
        v_s3 = total_calc_vol * (p_s3 / 100.0)
        v_s4 = total_calc_vol * (p_s4 / 100.0)
        
        cost_exc = (v_s1 * 45.0) + (v_s2 * 32.0) + (v_s3 * 22.0) + (v_s4 * 18.0)
        
        st.success(f"**Volumen Total de Excavación:** {total_calc_vol:,.1f} m³")
        st.write(f"- Excavación en Roca (S1): {v_s1:,.1f} m³ (Requiere Martillo/Explosivo)")
        st.write(f"- Excavación en Grava/Suelo (S2-S4): {v_s2 + v_s3 + v_s4:,.1f} m³")
        st.metric("Costo Estimado de Excavación Directa", f"${cost_exc:,.2f} USD")

# -----------------------------------------------------------------------------
# MODULE 4: SIMULADOR FINANCIERO CAPEX
# -----------------------------------------------------------------------------
elif module == "💰 Simulador Financiero CAPEX":
    st.markdown('<div class="main-header">Simulador Financiero y Análisis de Sensibilidad CAPEX</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Evaluación de Escenarios de Riesgo, Contingencias e Indirectos EPCM</div>', unsafe_allow_html=True)
    
    col_params, col_charts = st.columns([4, 6])
    
    with col_params:
        st.subheader("⚙️ Parámetros del Modelo Financiero")
        base_cost = summary_df["Direct_Cost_USD"].sum()
        
        st.write(f"**Costo Directo Base:** ${base_cost:,.0f} USD")
        
        contingency_pct = st.slider("Porcentaje de Contingencia de Proyecto (%):", 5.0, 30.0, 12.0, step=0.5)
        escalation_pct = st.slider("Escalación Precios Mercado Equipos Críticos (%):", -10.0, 25.0, 5.0, step=0.5)
        epcm_pct = st.slider("Gastos Indirectos, Ingeniería y EPCM (%):", 5.0, 18.0, 10.0, step=0.5)
        
        # Calculations
        escalation_val = base_cost * (escalation_pct / 100.0)
        subtotal_direct = base_cost + escalation_val
        epcm_val = subtotal_direct * (epcm_pct / 100.0)
        contingency_val = (subtotal_direct + epcm_val) * (contingency_pct / 100.0)
        total_capex_sim = subtotal_direct + epcm_val + contingency_val
        
        st.markdown("---")
        st.subheader("📊 Resultado del Escenario")
        st.metric("CAPEX TOTAL ESTIMADO", f"${total_capex_sim:,.0f} USD", delta=f"${total_capex_sim - base_cost:,.0f} USD vs Base")

    with col_charts:
        st.subheader("Desglose Waterfall del Presupuesto Proyecto")
        
        fig_waterfall = go.Figure(go.Waterfall(
            name="CAPEX",
            orientation="v",
            measure=["relative", "relative", "relative", "relative", "total"],
            x=["Costo Directo Base", "Escalación Suministros", "EPCM e Indirectos", "Reserva Contingencia", "CAPEX TOTAL"],
            textposition="outside",
            text=[f"${base_cost/1e6:.1f}M", f"${escalation_val/1e6:.1f}M", f"${epcm_val/1e6:.1f}M", f"${contingency_val/1e6:.1f}M", f"${total_capex_sim/1e6:.1f}M"],
            y=[base_cost, escalation_val, epcm_val, contingency_val, total_capex_sim],
            connector={"line": {"color": "rgb(63, 63, 63)"}},
            decreasing={"marker": {"color": "#10B981"}},
            increasing={"marker": {"color": "#EF4444"}},
            totals={"marker": {"color": "#1E3A8A"}}
        ))
        fig_waterfall.update_layout(height=420, margin=dict(l=20, r=20, t=30, b=20))
        st.plotly_chart(fig_waterfall, use_container_width=True)

# -----------------------------------------------------------------------------
# MODULE 5: SUMINISTROS CRÍTICOS (LONG LEAD)
# -----------------------------------------------------------------------------
elif module == "🚚 Suministros Críticos (Long Lead)":
    st.markdown('<div class="main-header">Monitoreo de Equipos Críticos (Long Lead Items)</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Seguimiento de Hitos de Fabricación, Pruebas FAT y Logística de Arribo a Mina Escondida</div>', unsafe_allow_html=True)
    
    st.dataframe(
        supplies_df.style.highlight_max(axis=0, subset=["Lead_Time_Meses"], color="#FCA5A5"),
        use_container_width=True
    )
    
    st.subheader("Línea de Tiempo de Arribo a Faena (2026 - 2027)")
    fig_gantt = px.bar(
        supplies_df,
        x="Lead_Time_Meses",
        y="Equipo",
        color="Estado_FAT",
        orientation="h",
        text="Arribo_Mina",
        labels={"Lead_Time_Meses": "Tiempo de Fabricación y Transporte (Meses)", "Equipo": "Suministro Crítico"}
    )
    fig_gantt.update_layout(height=380)
    st.plotly_chart(fig_gantt, use_container_width=True)

# -----------------------------------------------------------------------------
# MODULE 6: EXPORTACIÓN DE INFORMES
# -----------------------------------------------------------------------------
elif module == "📤 Exportación de Informes":
    st.markdown('<div class="main-header">Centro de Descarga de Informes y Datos</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Exportación de Tablas Maestras y Generación de Reportes Ejecutivos</div>', unsafe_allow_html=True)
    
    col_d1, col_d2 = st.columns(2)
    with col_d1:
        st.subheader("📥 Exportar Tabla de Cubicaciones (CSV)")
        csv_data = mto_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Descargar MTO Completo (CSV)",
            data=csv_data,
            file_name="BHP_ENC3430_MTO_Cubicaciones.csv",
            mime="text/csv"
        )
        
    with col_d2:
        st.subheader("📊 Exportar Resumen CAPEX (CSV)")
        csv_summary = summary_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Descargar Consolidado CAPEX (CSV)",
            data=csv_summary,
            file_name="BHP_ENC3430_CAPEX_Consolidado.csv",
            mime="text/csv"
        )

st.sidebar.markdown("---")
st.sidebar.caption("© 2026 BHP - Project Management System | ENC-3430 Class 3 Engineering")
