import streamlit as st
from datetime import datetime, timedelta

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(
    page_title="Sistema Areté - Promotoría",
    page_icon="🛡️",
    layout="wide"
)

# Aplicando la paleta corporativa mediante CSS personalizado (Azul Marino y Dorado Prestige)
st.markdown("""
    <style>
    .main {
        background-color: #FFFFFF;
    }
    h1, h2, h3 {
        color: #642342; /* Azul Marino Corporativo */
        font-family: 'Montserrat', sans-serif;
    }
    .stButton>button {
        background-color: #044343; /* Dorado Prestige / Acento */
        color: white;
        border-radius: 5px;
        font-weight: bold;
    }
    .metric-card {
        background-color: #f4f4f4;
        padding: 15px;
        border-radius: 8px;
        border-left: 5px solid #044343;
    }
    </style>
""", unsafe_allow_html=True)

# 2. LOGOTIPO Y TÍTULO
try:
    st.image("Arete Promotoria.jpg", width=220)
except:
    st.title("🛡️ Areté Promotoría")

st.title("Sistema de Gestión e Indicadores")
st.markdown("---")

# Menú lateral para navegación
menu = st.sidebar.selectbox("Navegación", ["Panel Directivo", "Registro de Pólizas", "Portal del Agente"])

# ---------------------------------------------------------
# SECCIÓN 1: PANEL DIRECTIVO
# ---------------------------------------------------------
if menu == "Panel Directivo":
    st.subheader("📊 Panel de Control Gerencial")
    
    # Selector con opción "Areté" para ver el total global y por aseguradora individual
    vista_seleccionada = st.selectbox(
        "Selecciona el Filtro de Visualización:", 
        ["Areté (Total Global)", "Afirme", "Ve por Más (Bx+)", "Insignia Life"]
    )
    
    col1, col2, col3 = st.columns(3)
    
    if vista_seleccionada == "Areté (Total Global)":
        with col1:
            st.markdown('<div class="metric-card"><h3>Producción Total Areté</h3><p><b>$0.00 MXN</b> (Suma de las 3)</p></div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="metric-card"><h3>Siniestralidad Global</h3><p><b>0.0%</b></p></div>', unsafe_allow_html=True)
        with col3:
            st.markdown('<div class="metric-card"><h3>Total Agentes Activos</h3><p><b>0 Registrados</b></p></div>', unsafe_allow_html=True)
        st.info("💡 Estás visualizando el **Consolidado Global de Areté**, sumando la operación de Afirme, Bx+ e Insignia Life.")
    else:
        with col1:
            st.markdown(f'<div class="metric-card"><h3>Producción ({vista_seleccionada})</h3><p><b>$0.00 MXN</b></p></div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div class="metric-card"><h3>Siniestralidad Autos</h3><p><b>0.0%</b></p></div>', unsafe_allow_html=True)
        with col3:
            st.markdown(f'<div class="metric-card"><h3>Agentes en {vista_seleccionada}</h3><p><b>0 Registrados</b></p></div>', unsafe_allow_html=True)
        st.info(f"💡 Visualizando los indicadores comerciales específicos para **{vista_seleccionada}**.")

# ---------------------------------------------------------
# SECCIÓN 2: REGISTRO DE PÓLIZAS
# ---------------------------------------------------------
elif menu == "Registro de Pólizas":
    st.subheader("📂 Alta de Póliza Nueva y Control de Vigencias")
    
    with st.form("form_poliza"):
        col_a, col_b = st.columns(2)
        with col_a:
            num_poliza = st.text_input("Número de Póliza")
            aseguradora_poliza = st.selectbox("Aseguradora", ["Afirme", "Ve por Más (Bx+)", "Insignia Life"])
            ramo = st.selectbox("Ramo", ["Autos", "Daños", "Vida"])
            nombre_cliente = st.text_input("Nombre del Asegurado / Cliente")
        with col_b:
            prima_neta = st.number_input("Prima Neta Pagada (MXN)", min_value=0.0, format="%.2f")
            fecha_inicio = st.date_input("Fecha de Inicio de Vigencia", value=datetime.today())
            fecha_vencimiento = st.date_input("Fecha de Fin de Vigencia", value=datetime.today() + timedelta(days=365))
            periodicidad = st.selectbox("Periodicidad de Pago", ["Anual", "Semestral", "Trimestral", "Mensual"])
            
        submitted = st.form_submit_button("Guardar y Calendarizar Alertas")
        
        if submitted:
            st.success(f"¡Póliza {num_poliza} registrada con éxito! Periodicidad: **{periodicidad}**. Alertas programadas para Ejecutivo de Cobranza, Agente y Asegurado.")

# ---------------------------------------------------------
# SECCIÓN 3: PORTAL DEL AGENTE
# ---------------------------------------------------------
elif menu == "Portal del Agente":
    st.subheader("👤 Vista de Agente - Semáforo de Metas")
    
    st.markdown("### 🎯 Tu Avance Trimestral")
    st.progress(0.15)
    st.write("Prima Acumulada: $150,000 / Meta Banda: $300,000 MXN")
    
    st.markdown("### ✈️ Camino a Convención (Con Potenciador Nueva Recluta)")
    st.progress(0.40)
    st.write("Estatus: En trayecto hacia la Convención Premier Nacional.")
