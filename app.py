import streamlit as st
from datetime import datetime, timedelta

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(
    page_title="Sistema Areté - Promotoría",
    page_icon="🛡️",
    layout="wide"
)

# Estilos con la identidad corporativa de Areté (Azul Marino y Dorado Prestige)
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
        background-color: #044343; /* Dorado Prestige */
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
    st.image("logo_arete.png", width=220)
except:
    st.title("🛡️ Areté Promotoría")

st.title("Sistema de Gestión e Indicadores")
st.markdown("---")

# Menú lateral
menu = st.sidebar.selectbox("Navegación", ["Panel Directivo", "Registro de Pólizas", "Portal del Agente"])

# ---------------------------------------------------------
# SECCIÓN 1: PANEL DIRECTIVO
# ---------------------------------------------------------
if menu == "Panel Directivo":
    st.subheader("📊 Panel de Control Gerencial")
    
    vista_seleccionada = st.selectbox(
        "Selecciona el Filtro de Visualización:", 
        ["Areté (Total Global)", "Afirme", "Ve por Más (Bx+)", "Insignia Life"]
    )
    
    col1, col2, col3 = st.columns(3)
    
    if vista_seleccionada == "Areté (Total Global)":
        with col1:
            st.markdown('<div class="metric-card"><h3>Producción Total Areté</h3><p><b>$0.00 MXN</b></p></div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="metric-card"><h3>Siniestralidad Global</h3><p><b>0.0%</b></p></div>', unsafe_allow_html=True)
        with col3:
            st.markdown('<div class="metric-card"><h3>Total Agentes Activos</h3><p><b>0 Registrados</b></p></div>', unsafe_allow_html=True)
        st.info("💡 Consolidado Global de Areté (Afirme, Bx+ e Insignia Life).")
    else:
        with col1:
            st.markdown(f'<div class="metric-card"><h3>Producción ({vista_seleccionada})</h3><p><b>$0.00 MXN</b></p></div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div class="metric-card"><h3>Siniestralidad</h3><p><b>0.0%</b></p></div>', unsafe_allow_html=True)
        with col3:
            st.markdown(f'<div class="metric-card"><h3>Agentes Activos</h3><p><b>0 Registrados</b></p></div>', unsafe_allow_html=True)
        st.info(f"💡 Visualizando indicadores comerciales para **{vista_seleccionada}**.")

# ---------------------------------------------------------
# SECCIÓN 2: REGISTRO DE PÓLIZAS CON MOTOR DE CÁLCULO INSIGNIA LIFE
# ---------------------------------------------------------
elif menu == "Registro de Pólizas":
    st.subheader("📂 Alta de Póliza y Cálculo de Prima Computable")
    
    with st.form("form_poliza"):
        col_a, col_b = st.columns(2)
        with col_a:
            num_poliza = st.text_input("Número de Póliza")
            aseguradora_poliza = st.selectbox("Aseguradora", ["Insignia Life", "Afirme", "Ve por Más (Bx+)"])
            nombre_cliente = st.text_input("Nombre del Asegurado / Cliente")
            
            # Campos específicos según aseguradora
            if aseguradora_poliza == "Insignia Life":
                producto_insignia = st.selectbox("Producto Insignia Life", [
                    "Vida 90", 
                    "Temporales", 
                    "Vitalicios y VPL", 
                    "Insignia Life Universal / DotIL", 
                    "Insignia Life Universal +"
                ])
                plazo_pago = st.number_input("Plazo de Pago de Primas (Años)", min_value=1, max_value=30, value=10)
            else:
                producto_insignia = "N/A"
                plazo_pago = 1.0

        with col_b:
            prima_neta = st.number_input("Prima Neta Pagada (MXN)", min_value=0.0, format="%.2f")
            fecha_inicio = st.date_input("Fecha de Inicio de Vigencia", value=datetime.today())
            fecha_vencimiento = st.date_input("Fecha de Fin de Vigencia", value=datetime.today() + timedelta(days=365))
            periodicidad = st.selectbox("Periodicidad de Pago", ["Anual", "Semestral", "Trimestral", "Mensual"])
            
        submitted = st.form_submit_button("Guardar Póliza y Calcular")
        
        if submitted:
            # Lógica de cálculo de Prima Computable basada en el cuaderno de Insignia Life
            factor_ponderacion = 1.0
            if aseguradora_poliza == "Insignia Life":
                if producto_insignia == "Vida 90":
                    factor_ponderacion = 0.20 if plazo_pago <= 4 else 1.0 # Ejemplo normativo del cuaderno
                elif producto_insignia == "Vitalicios y VPL":
                    factor_ponderacion = 0.05 if plazo_pago <= 4 else (0.40 if plazo_pago <= 9 else (0.80 if plazo_pago <= 14 else 1.0))
                elif "Universal" in producto_insignia:
                    factor_ponderacion = 0.80 if plazo_pago < 15 else 1.0
            
            prima_computable = prima_neta * factor_ponderacion
            
            st.success(f"¡Póliza {num_poliza} registrada con éxito!")
            st.info(f"📊 **Análisis Insignia Life:** Prima Neta: ${prima_neta:,.2f} | Factor Aplicado: {int(factor_ponderacion*100)}% | **Prima Computable para Bonos: ${prima_computable:,.2f} MXN**")

# ---------------------------------------------------------
# SECCIÓN 3: PORTAL DEL AGENTE
# ---------------------------------------------------------
elif menu == "Portal del Agente":
    st.subheader("👤 Vista de Agente - Semáforo de Metas y Bonos")
    
    st.markdown("### 🎯 Tu Avance Trimestral (Insignia Life / Afirme)")
    st.progress(0.15)
    st.write("Prima Computable Acumulada: $150,000 / Meta Banda Requerida: $465,000 MXN")
    
    st.markdown("### ✈️ Camino a Convención Anual 2027")
    st.progress(0.40)
    st.write("Estatus: En trayecto hacia la Convención Top Estelar.")
