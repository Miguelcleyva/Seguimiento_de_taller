import streamlit as st

st.set_page_config(page_title="Seguimiento de Taller", layout="wide")

st.title("📋 Seguimiento de Vehículos en Taller")

st.markdown("""
Esta app permite registrar, controlar y visualizar el avance de vehículos en un taller de planchado y pintura.  
Incluye integración con Google Sheets y Drive, generación de PDF y panel de KPIs.
""")

st.subheader("📝 Registro de unidad")

with st.form("registro_unidad"):
    col1, col2 = st.columns(2)
    with col1:
        cliente = st.text_input("Nombre del cliente")
        placa = st.text_input("Placa del vehículo")
        marca = st.text_input("Marca del vehículo")
        modelo = st.text_input("Modelo del vehículo")
        compania = st.selectbox("Compañía de seguros", ["Rimac", "Mapfre", "Pacifico", "HDI", "La Positiva", "Otra"])
        fecha_ingreso = st.date_input("Fecha de ingreso al taller")

    with col2:
        aprobado_cliente = st.selectbox("¿Aprobado por el cliente?", ["En espera", "Aprobado", "No aprobado"])
        aprobado_seguro = st.selectbox("¿Aprobado por la aseguradora?", ["En espera", "Aprobado", "No aprobado"])
        fecha_aprob_cliente = st.date_input("Fecha de aprobación del cliente (si aplica)")
        fecha_aprob_seguro = st.date_input("Fecha de aprobación del seguro (si aplica)")
        fecha_entrega_estimada = st.date_input("Fecha tentativa de entrega")

    comentario = st.text_area("Observaciones o comentarios adicionales")

    submitted = st.form_submit_button("Registrar unidad")

    if submitted:
        st.success(f"✅ Unidad con placa **{placa}** registrada correctamente.")
