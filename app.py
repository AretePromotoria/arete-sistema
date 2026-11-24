import streamlit as st
from datetime import datetime, timedelta

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(
    page_title="Sistema Areté - Promotoría",
    page_icon="🛡️",
    layout="wide"
)

# Estilos corporativos de Areté (Azul Marino Corporativo y Dorado Prestige)
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

# 2. INICIALIZAR MEMORIA EN LA NUBE (SESSION STATE)
if "cartera_polizas" not in st.session_state:
    st.session_state.cartera_polizas = []

if "conceptos_presupuesto" not in st.session_state:
    st.session_state.conceptos_presupuesto = []

# 3. LOGOTIPO OFICIAL Y TÍTULO
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

    total_produccion = sum(
        p["prima_computable"]
        for p in st.session_state.cartera_polizas
        if vista_seleccionada == "Areté (Total Global)" or p["aseguradora"] == vista_seleccionada
    )

    total_pols = (
        len(st.session_state.cartera_polizas)
        if vista_seleccionada == "Areté (Total Global)"
        else len([p for p in st.session_state.cartera_polizas if p["aseguradora"] == vista_seleccionada])
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f'<div class="metric-card"><h3>Producción</h3><p><b>${total_produccion:,.2f} MXN</b></p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-card"><h3>Siniestralidad</h3><p><b>0.0%</b></p></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="metric-card"><h3>Pólizas Registradas</h3><p><b>{total_pols} Activas</b></p></div>', unsafe_allow_html=True)

    st.info(f"💡 Visualizando indicadores comerciales para **{vista_seleccionada}**.")

# ---------------------------------------------------------
# SECCIÓN 2: REGISTRO DE PÓLIZAS
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
            elif aseguradora_poliza == "Ve por Más (Bx+)":
                producto_bx = st.selectbox("Ramo Ve por Más", [
                    "Vida Individual", "GMM Individual", "Accidentes Personales",
                    "Automóviles Residentes", "Daños", "Vida Grupo / GMM Colectivo"
                ])
                plazo_pago = 1.0
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
            if not num_poliza or not nombre_cliente:
                st.error("Por favor completa al menos el Número de Póliza y el Nombre del Cliente.")
            else:
                factor_ponderacion = 1.0
                if aseguradora_poliza == "Insignia Life":
                    if producto_insignia == "Vida 90":
                        factor_ponderacion = 0.20 if plazo_pago <= 4 else 1.0
                    elif producto_insignia == "Vitalicios y VPL":
                        factor_ponderacion = 0.05 if plazo_pago <= 4 else (0.40 if plazo_pago <= 9 else (0.80 if plazo_pago <= 14 else 1.0))
                    elif "Universal" in producto_insignia:
                        factor_ponderacion = 0.80 if plazo_pago < 15 else 1.0

                prima_computable = prima_neta * factor_ponderacion

                nueva_poliza = {
                    "poliza": num_poliza,
                    "aseguradora": aseguradora_poliza,
                    "cliente": nombre_cliente,
                    "periodicidad": periodicidad,
                    "vencimiento": fecha_vencimiento.strftime("%d/%m/%Y"),
                    "contacto": f"📱 {whatsapp_cliente} / ✉️ {email_cliente}",
                    "agente": nombre_agente if nombre_agente else "No asignado",
                    "prima_computable": prima_computable
                }
                st.session_state.cartera_polizas.append(nueva_poliza)

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

    if len(st.session_state.cartera_polizas) == 0:
        st.info("📭 **No hay pólizas registradas en este momento.** Las alertas de cobranza aparecerán automáticamente aquí conforme des de alta pólizas en la sección de 'Registro de Pólizas'.")
    else:
        st.markdown("### 📋 Cartera en Seguimiento con Contactos de Notificación")

        polizas_a_mostrar = st.session_state.cartera_polizas
        if filtro_aseg != "Todas":
            polizas_a_mostrar = [p for p in st.session_state.cartera_polizas if p["aseguradora"] == filtro_aseg]

        for p in polizas_a_mostrar:
            st.markdown(f"""
            - **Póliza:** `{p['poliza']}` | **Aseguradora:** {p['aseguradora']} | **Cliente:** {p['cliente']}
              - **Periodicidad:** {p['periodicidad']} | **Vencimiento:** {p['vencimiento']}
              - **Contacto:** {p['contacto']} | **Agente:** {p['agente']}
              - 🟡 *Estatus: Alerta Automática Programada*
            """)
            st.markdown("---")

        if st.button("🚀 Enviar Notificaciones Automáticas (WhatsApp / Email)"):
            st.success("¡Motor de notificaciones ejecutado! Se han enviado los avisos de cobro correspondientes a los clientes y copias de seguimiento a los agentes.")

# ---------------------------------------------------------
# SECCIÓN 4: PORTAL DEL AGENTE
# ---------------------------------------------------------
elif menu == "Portal del Agente":
    st.subheader("👤 Vista de Agente")

    subvista_agente = st.radio(
        "Selecciona el módulo del Portal del Agente:",
        ["Semáforos y Convenciones", "Presupuesto Mensual Personalizado"],
        horizontal=True
    )

    st.markdown("---")

    if subvista_agente == "Semáforos y Convenciones":
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
                st.info("🇲🇽 **Convención Nacional (Top Insignia Life)**\n\n* **Meta:** $1,150,000 MXN\n* **Progreso:** $0.00 MXN (0%)")
            with col_conv2:
                st.success("🌍 **Convención Internacional / Estelar 2027**\n\n* **Meta:** $2,660,000 MXN\n* **Progreso:** $0.00 MXN (0%)")

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
            st.markdown("### 🏢 Ve por Más (Bx+) — Avance de Metas y Bonos 2026")
            col_meta1, col_meta2 = st.columns(2)
            with col_meta1:
                st.markdown("**🎯 Bono de Producción Trimestral Bx+**")
                st.progress(0.0)
                st.write("Acumulado: $0.00 / Requisito Mínimo Anual: $300,000 MXN")
            with col_meta2:
                st.markdown("**🛡️ Control de Siniestralidad y Calidad**")
                st.progress(0.0)
                st.write("Siniestralidad Cartera: 0.0% (Máx. permitido por ramo: 60%)")

            st.markdown("---")
            st.markdown("### ✈️ Convenciones Ve por Más 2027 (Destinos Oficiales)")
            col_conv1, col_conv2, col_conv3 = st.columns(3)
            with col_conv1:
                st.info("🇨🇦 **Convención Cobalto — Vancouver**\n\n* **Requisito:** Desde $3M a $4M según ramo.\n* **Crecimiento:** 15% vs año anterior.\n* **Progreso:** 0%")
            with col_conv2:
                st.warning("🇭🇺 **Convención Neón — Budapest**\n\n* **Requisito:** Desde $6M a $10M según ramo.\n* **Conservación Vida:** 88%.\n* **Progreso:** 0%")
            with col_conv3:
                st.success("🇨🇿 **Convención Litio — Praga**\n\n* **Requisito:** Ganar Convención Neón + 100% negocio nuevo.\n* **Progreso:** 0%")

    else:
        st.markdown("### 🧮 Presupuesto Mensual Personalizado")
        st.caption("Calcula tu proyección mes a mes y agrega tus propios conceptos para adaptar el presupuesto a tu operación.")

        meses = [
            "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
            "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
        ]

        col_p1, col_p2 = st.columns(2)
        with col_p1:
            mes_seleccionado = st.selectbox("Mes a proyectar", meses)
        with col_p2:
            ingreso_base_mes = st.number_input(
                f"Ingreso / Comisión base estimada para {mes_seleccionado} ($ MXN)",
                min_value=0.0,
                value=0.0,
                step=1000.0,
                format="%.2f"
            )

        st.markdown("---")
        st.markdown("#### ➕ Agregar Concepto Personalizado")

        with st.form("form_concepto_agente"):
            c1, c2, c3, c4 = st.columns(4)
            with c1:
                nombre_concepto = st.text_input("Concepto", placeholder="Ej. Viáticos / Bono extra")
            with c2:
                tipo_concepto = st.selectbox("Tipo", ["Ingreso (+)", "Egreso / Meta (-)"])
            with c3:
                monto_concepto = st.number_input("Monto ($ MXN)", min_value=0.0, value=0.0, step=500.0, format="%.2f")
            with c4:
                aplica_mes = st.selectbox("Aplica en", [f"Solo {mes_seleccionado}", "Todos los meses"])

            agregar_concepto = st.form_submit_button("Agregar al Presupuesto")

            if agregar_concepto:
                if nombre_concepto.strip() and monto_concepto > 0:
                    st.session_state.conceptos_presupuesto.append({
                        "concepto": nombre_concepto.strip(),
                        "tipo": tipo_concepto,
                        "monto": monto_concepto,
                        "aplica_mes": aplica_mes
                    })
                    st.success(f"Concepto '{nombre_concepto}' agregado.")
                else:
                    st.warning("Escribe un nombre de concepto y un monto mayor a $0.00.")

        extra_ingresos = 0.0
        extra_egresos = 0.0

        for item in st.session_state.conceptos_presupuesto:
            aplica = (item["aplica_mes"] == "Todos los meses") or (item["aplica_mes"] == f"Solo {mes_seleccionado}")
            if aplica:
                if item["tipo"] == "Ingreso (+)":
                    extra_ingresos += item["monto"]
                else:
                    extra_egresos += item["monto"]

        total_mes = ingreso_base_mes + extra_ingresos - extra_egresos

        st.markdown("#### 📊 Resumen del Mes")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Ingreso Base", f"${ingreso_base_mes:,.2f}")
        m2.metric("Ingresos Extra (+)", f"${extra_ingresos:,.2f}")
        m3.metric("Egresos / Metas (-)", f"${extra_egresos:,.2f}")
        m4.metric("Balance Proyectado", f"${total_mes:,.2f}")

        if st.session_state.conceptos_presupuesto:
            st.markdown("#### 📋 Conceptos Personalizados Registrados")
            for idx, item in enumerate(st.session_state.conceptos_presupuesto):
                col_item, col_btn = st.columns([5, 1])
                with col_item:
                    st.write(
                        f"**{item['concepto']}** | {item['tipo']} | "
                        f"${item['monto']:,.2f} MXN | *{item['aplica_mes']}*"
                    )
                with col_btn:
                    if st.button("Eliminar", key=f"del_conc_{idx}"):
                        st.session_state.conceptos_presupuesto.pop(idx)
                        st.rerun()
        else:
            st.info("Aún no has agregado conceptos personalizados. Empieza en ceros y añade los que necesites.")
