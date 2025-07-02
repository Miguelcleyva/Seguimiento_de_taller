import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime
import json
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
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds_dict = st.secrets["gcp_service_account"]
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
        client = gspread.authorize(creds)

        # Abre tu hoja de cálculo
        sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1rCYR_jhWeqEQVY5N4e_Aeje-6oop310PquvqPYKB9NE")
        worksheet = sheet.worksheet("Registro")  # Asegúrate que esta hoja exista

        # Prepara los datos
        nueva_fila = [
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            cliente, placa, marca, modelo, compania,
            str(fecha_ingreso), aprobado_cliente, aprobado_seguro,
            str(fecha_aprob_cliente), str(fecha_aprob_seguro),
            str(fecha_entrega_estimada), comentario
        ]

        # Agrega la fila
        worksheet.append_row(nueva_fila)

        st.success(f"✅ Unidad con placa **{placa}** registrada y guardada en Google Sheets.")

