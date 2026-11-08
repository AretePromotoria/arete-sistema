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

# 2. LOGOTIPO OFICIAL Y TÍTULO
try:
    st.image("Arete Promotoria.jpg", width=220)
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
# SECCIÓN 2: REGISTRO DE PÓLIZAS CON CÁLCULO
# ---------------------------------------------------------
elif menu == "Registro de Pólizas":
    st.subheader("📂 Alta de Póliza y Control de Vigencias")
    
    with st.form("form_poliza"):
        col_a, col_b = st.columns(2)
        with col_a:
            num_poliza = st.text_input("Número de Póliza")
            aseguradora_poliza = st.selectbox("Aseguradora", ["Insignia Life", "Afirme", "Ve por Más (Bx+)"])
            nombre_cliente = st.text_input("Nombre del Asegurado / Cliente")
            
            if aseguradora_poliza == "Insignia Life":
                producto_insignia = st.selectbox("Producto Insignia Life", [
                    "Vida 90", "Temporales", "Vitalicios y VPL", 
                    "Insignia Life Universal / DotIL", "Insignia Life Universal +"
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
            
        submitted = st.form_submit_button("Guardar Póliza y Calendarizar")
        
        if submitted:
            factor_ponderacion = 1.0
            if aseguradora_poliza == "Insignia Life":
                if producto_insignia == "Vida 90":
                    factor_ponderacion = 0.20 if plazo_pago <= 4 else 1.0
                elif producto_insignia == "Vitalicios y VPL":
                    factor_ponderacion = 0.05 if plazo_pago <= 4 else (0.40 if plazo_pago <= 9 else (0.80 if plazo_pago <= 14 else 1.0))
                elif "Universal" in producto_insignia:
                    factor_ponderacion = 0.80 if plazo_pago < 15 else 1.0
            
            prima_computable = prima_neta * factor_ponderacion
            st.success(f"¡Póliza {num_poliza} registrada con éxito!")
            st.info(f"📊 **Análisis:** Prima Neta: ${prima_neta:,.2f} | **Prima Computable: ${prima_computable:,.2f} MXN** | Alertas configuradas para periodicidad **{periodicidad}**.")

# ---------------------------------------------------------
# SECCIÓN 3: PORTAL DEL AGENTE (SEPARADO POR ASEGURADORA)
# ---------------------------------------------------------
elif menu == "Portal del Agente":
    st.subheader("👤 Vista de Agente - Semáforos y Convenciones por Aseguradora")
    
    agente_aseguradora = st.selectbox(
        "Selecciona la Aseguradora para consultar tus Metas y Convenciones:", 
        ["Insigina Life", "Afirme", "Ve por Más (Bx+)"]
    )
    
    st.markdown("---")
    
    if agente_aseguradora == "Insigina Life":
        st.markdown("### 🏢 Insignia Life — Avance de Metas")
        col_meta1, col_meta2 = st.columns(2)
        with col_meta1:
            st.markdown("**🎯 Bono Trimestral / Anual (Vida Individual)**")
            st.progress(0.15)
            st.write("Acumulado: $150,000 / Meta Banda: $465,000 MXN")
        with col_meta2:
            st.markdown("**🛡️ Índice de Conservación**")
            st.progress(0.90)
            st.write("Estatus Actual: 90.0% (Requerido > 87.5%)")
            
        st.markdown("---")
        st.markdown("### ✈️ Convenciones Insignia Life 2027")
        col_conv1, col_conv2 = st.columns(2)
        with col_conv1:
            st.info("🇲🇽 **Convención Nacional (Top Insignia Life)**\n\n* **Meta:** $1,150,000 MXN\n* **Progreso:** $350,000 MXN (30%)\n* *Estatus: En ruta*")
        with col_conv2:
            st.success("🌍 **Convención Internacional / Estelar 2027**\n\n* **Meta:** $2,660,000 MXN\n* **Progreso:** $350,000 MXN (13%)\n* *Estatus: En desarrollo*")

    elif agente_aseguradora == "Afirme":
        st.markdown("### 🏢 Afirme — Avance de Metas")
        col_meta1, col_meta2 = st.columns(2)
        with col_meta1:
            st.markdown("**🎯 Bono Mensual / Trimestral Autos y Vida**")
            st.progress(0.45)
            st.write("Acumulado: $750,000 / Meta Banda: $1,500,000 MXN")
        with col_meta2:
            st.markdown("**📉 Siniestralidad de Cartera**")
            st.progress(0.38)
            st.write("Estatus Actual: 38% (Meta < 40%)")
            
        st.markdown("---")
        st.markdown("### ✈️ Convenciones Afirme")
        col_conv1, col_conv2 = st.columns(2)
        with col_conv1:
            st.info("🇲🇽 **Convención Nacional Afirme**\n\n* **Progreso:** 50% alcanzado hacia la meta anual.")
        with col_conv2:
            st.success("🌍 **Convención Estelar Internacional Afirme**\n\n* **Progreso:** 25% alcanzado hacia el objetivo.")

    else:
        st.markdown("### 🏢 Ve por Más (Bx+) — Avance de Metas")
        col_meta1, col_meta2 = st.columns(2)
        with col_meta1:
            st.markdown("**🎯 Bono de Producción Bx+**")
            st.progress(0.20)
            st.write("Estatus de primas computables vigentes.")
        with col_meta2:
            st.markdown("**🛡️ Retención y Conservación**")
            st.progress(0.85)
            st.write("Estatus óptimo de cartera.")
            
        st.markdown("---")
        st.markdown("### ✈️ Convenciones Ve por Más (Bx+)")
        col_conv1, col_conv2 = st.columns(2)
        with col_conv1:
            st.info("🇲🇽 **Convención Nacional Bx+**\n\n* Seguimiento de objetivos anuales.")
        with col_conv2:
            st.success("🌍 **Convención Internacional Bx+**\n\n* Trayectoria hacia el reconocimiento global.")
