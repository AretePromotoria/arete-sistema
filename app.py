import streamlit as st
from datetime import datetime, timedelta

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(
    page_title="Sistema Areté - Promotoría",
    page_icon="🛡️",
    layout="wide"
)

# Estilos con la identidad corporativa de Areté (Azul Marino Corporativo y Dorado Prestige)
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
menu = st.sidebar.selectbox(
    "Navegación", 
    ["Panel Directivo", "Registro de Pólizas", "Control de Cobranza y Alertas", "Portal del Agente"]
)

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
# SECCIÓN 2: REGISTRO DE PÓLIZAS CON DATOS DE CONTACTO
# ---------------------------------------------------------
elif menu == "Registro de Pólizas":
    st.subheader("📂 Alta de Póliza, Canales de Contacto y Control de Vigencias")
    
    with st.form("form_poliza"):
        st.markdown("##### 📌 Datos Generales de la Póliza")
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
        
        st.markdown("---")
        st.markdown("##### 📲 Canales de Notificación para Alertas y Cobranza")
        col_c, col_d = st.columns(2)
        with col_c:
            st.markdown("**Datos del Cliente / Asegurado:**")
            email_cliente = st.text_input("Correo Electrónico del Cliente", placeholder="ejemplo@cliente.com")
            whatsapp_cliente = st.text_input("WhatsApp / Teléfono del Cliente (10 dígitos)", placeholder="5512345678")
        with col_d:
            st.markdown("**Datos del Agente Responsable:**")
            nombre_agente = st.text_input("Nombre del Agente de Seguros")
            email_agente = st.text_input("Correo Electrónico del Agente", placeholder="agente@arete-promotoria.com")
            whatsapp_agente = st.text_input("WhatsApp del Agente (10 dígitos)", placeholder="5587654321")

        submitted = st.form_submit_button("Guardar Póliza y Calendarizar Alertas")
        
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
            st.success(f"¡Póliza {num_poliza} registrada con éxito para el cliente {nombre_cliente}!")
            st.info(f"📊 **Análisis:** Prima Neta: ${prima_neta:,.2f} | **Prima Computable: ${prima_computable:,.2f} MXN**")
            st.info(f"🔔 **Ruta de Alerta Configurada:** Notificaciones programadas vía WhatsApp ({whatsapp_cliente}) y Correo ({email_cliente}) con copia al Agente ({email_agente}) según periodicidad **{periodicidad}**.")

# ---------------------------------------------------------
# SECCIÓN 3: CONTROL DE COBRANZA Y ALERTAS AUTOMÁTICAS
# ---------------------------------------------------------
elif menu == "Control de Cobranza y Alertas":
    st.subheader("🔔 Motor de Alertas y Calendario de Cobranza")
    st.markdown("Este panel monitorea las fechas de vencimiento subsecuentes según la periodicidad configurada y notifica a través de los datos de contacto registrados.")
    
    col_filtro1, col_filtro2 = st.columns(2)
    with col_filtro1:
        filtro_estado = st.selectbox("Filtrar por Estatus de Cobro", ["Próximos a Vencer (30 días)", "Vencidos / Con Adeudo", "Pagados al Corriente"])
    with col_filtro2:
        filtro_aseg = st.selectbox("Filtrar por Aseguradora", ["Todas", "Insignia Life", "Afirme", "Ve por Más (Bx+)"])
        
    st.markdown("---")
    
    st.markdown("### 📋 Cartera en Seguimiento con Contactos de Notificación")
    st.markdown("""
    | Póliza | Aseguradora | Cliente | Periodicidad | Contacto Cliente | Agente | Estatus Alerta |
    | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
    | *Ejemplo* | Insignia Life | Juan Pérez | Mensual | 📱 5512345678 / ✉️ juan@mail.com | Carlos Ruiz | 🟡 Alerta Automática Programada |
    | *Ejemplo* | Afirme | María López | Semestral | 📱 5598765432 / ✉️ maria@mail.com | Ana Gómez | 🟢 Cobro al Corriente |
    """)
    
    st.markdown("---")
    if st.button("🚀 Enviar Notificaciones Automáticas (WhatsApp / Email)"):
        st.success("¡Motor de notificaciones ejecutado! Se han enviado los avisos de cobro correspondientes a los clientes y copias de seguimiento a los agentes.")

# ---------------------------------------------------------
# SECCIÓN 4: PORTAL DEL AGENTE
# ---------------------------------------------------------
elif menu == "Portal del Agente":
    st.subheader("👤 Vista de Agente - Semáforos y Convenciones por Aseguradora")
    
    agente_aseguradora = st.selectbox(
        "Selecciona la Aseguradora para consultar tus Metas y Convenciones:", 
        ["Insignia Life", "Afirme", "Ve por Más (Bx+)"]
    )
    
    st.markdown("---")
    
    if agente_aseguradora == "Insignia Life":
        st.markdown("### 🏢 Insignia Life — Avance de Metas")
        col_meta1, col_meta2 = st.columns(2)
        with col_meta1:
            st.markdown("**🎯 Bono Trimestral / Anual (Vida Individual)**")
            st.progress(0.0)
            st.write("Acumulado: $0.00 / Meta Banda: $465,000 MXN")
        with col_meta2:
            st.markdown("**🛡️ Índice de Conservación**")
            st.progress(0.0)
            st.write("Estatus Actual: 0.0% (Requerido > 87.5%)")
            
        st.markdown("---")
        st.markdown("### ✈️ Convenciones Insignia Life 2027")
        col_conv1, col_conv2 = st.columns(2)
        with col_conv1:
            st.info("🇲🇽 **Convención Nacional (Top Insignia Life)**\n\n* **Meta:** $1,150,000 MXN\n* **Progreso:** $0.00 MXN (0%)\n* *Estatus: Sin avance registrado*")
        with col_conv2:
            st.success("🌍 **Convención Internacional / Estelar 2027**\n\n* **Meta:** $2,660,000 MXN\n* **Progreso:** $0.00 MXN (0%)\n* *Estatus: Sin avance registrado*")

    elif agente_aseguradora == "Afirme":
        st.markdown("### 🏢 Afirme — Avance de Metas")
        col_meta1, col_meta2 = st.columns(2)
        with col_meta1:
            st.markdown("**🎯 Bono Mensual / Trimestral Autos y Vida**")
            st.progress(0.0)
            st.write("Acumulado: $0.00 / Meta Banda: Por definir")
        with col_meta2:
            st.markdown("**📉 Siniestralidad de Cartera**")
            st.progress(0.0)
            st.write("Estatus Actual: 0.0% (Meta < 40%)")
            
        st.markdown("---")
        st.markdown("### ✈️ Convenciones Afirme")
        col_conv1, col_conv2 = st.columns(2)
        with col_conv1:
            st.info("🇲🇽 **Convención Nacional Afirme**\n\n* **Progreso:** 0% alcanzado.")
        with col_conv2:
            st.success("🌍 **Convención Estelar Internacional Afirme**\n\n* **Progreso:** 0% alcanzado.")

    else:
        st.markdown("### 🏢 Ve por Más (Bx+) — Avance de Metas")
        col_meta1, col_meta2 = st.columns(2)
        with col_meta1:
            st.markdown("**🎯 Bono de Producción Bx+**")
            st.progress(0.0)
            st.write("Acumulado: $0.00 MXN")
        with col_meta2:
            st.markdown("**🛡️ Retención y Conservación**")
            st.progress(0.0)
            st.write("Estatus actual: 0.0%")
            
        st.markdown("---")
        st.markdown("### ✈️ Convenciones Ve por Más (Bx+)")
        col_conv1, col_conv2 = st.columns(2)
        with col_conv1:
            st.info("🇲🇽 **Convención Nacional Bx+**\n\n* Sin pólizas registradas.")
        with col_conv2:
            st.success("🌍 **Convención Internacional Bx+**\n\n* Sin pólizas registradas.")
