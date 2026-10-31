import streamlit as st

# 1. LA CONFIGURACIÓN DE LA PÁGINA VA PRIMERO OBLIGATORIAMENTE
st.set_page_config(
    page_title="Sistema Areté - Promotoría",
    page_icon="🛡️",
    layout="wide"
)

# Aplicando la paleta corporativa mediante CSS personalizado
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

# 2. AHORA SÍ, MOSTRAMOS EL LOGOTIPO OFICIAL Y TÍTULO
# (Asegúrate de que tu imagen en GitHub se llame exactamente 'Arete Promotoria.jpg' 
# o cambia el texto de abajo por el nombre real que le pusiste al archivo)
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
    
    aseguradora = st.selectbox("Selecciona la Aseguradora a Monitorear:", ["Afirme", "Ve por Más (Bx+)", "Insignia Life"])
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="metric-card"><h3>Producción Global</h3><p><b>$0.00 MXN</b></p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-card"><h3>Siniestralidad Autos</h3><p><b>0.0%</b> (Meta < 65%)</p></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-card"><h3>Agentes Activos</h3><p><b>0 Registrados</b></p></div>', unsafe_allow_html=True)
        
    st.markdown("---")
    st.info(f"💡 Visualizando los indicadores comerciales actuales para **{aseguradora}**.")

# ---------------------------------------------------------
# SECCIÓN 2: REGISTRO DE PÓLIZAS
# ---------------------------------------------------------
elif menu == "Registro de Pólizas":
    st.subheader("📂 Alta de Póliza Nueva")
    
    with st.form("form_poliza"):
        col_a, col_b = st.columns(2)
        with col_a:
            num_poliza = st.text_input("Número de Póliza")
            aseguradora_poliza = st.selectbox("Aseguradora", ["Afirme", "Ve por Más (Bx+)", "Insignia Life"])
            ramo = st.selectbox("Ramo", ["Autos", "Daños", "Vida"])
        with col_b:
            nombre_cliente = st.text_input("Nombre del Asegurado / Cliente")
            prima_neta = st.number_input("Prima Neta Pagada (MXN)", min_value=0.0, format="%.2f")
            fecha_vencimiento = st.date_input("Fecha de Vencimiento")
            
        submitted = st.form_submit_button("Guardar y Calcular Bonos")
        
        if submitted:
            st.success(f"¡Póliza {num_poliza} registrada con éxito!")

# ---------------------------------------------------------
# SECCIÓN 3: PORTAL DEL AGENTE
# ---------------------------------------------------------
elif menu == "Portal del Agente":
    st.subheader("👤 Vista de Agente - Semáforo de Metas")
    
    st.markdown("### 🎯 Tu Avance Trimestral (Afirme)")
    st.progress(0.15)
    st.write("Prima Acumulada: $150,000 / Meta Banda: $300,000 MXN")
    
    st.markdown("### ✈️ Camino a Convención (Con Potenciador Nueva Recluta)")
    st.progress(0.40)
    st.write("Estatus: En trayecto hacia la Convención Premier Nacional.")
