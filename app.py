import streamlit as st

st.set_page_config(page_title="Seguimiento de Taller", layout="wide")

st.title("📋 Seguimiento de Vehículos en Taller")
st.write("Bienvenido, selecciona una acción desde la barra lateral.")

streamlit
gspread
oauth2client
pandas
python-docx
python-dateutil
reportlab

# App de Seguimiento de Taller

Esta app permite registrar, controlar y visualizar el avance de vehículos en un taller de planchado y pintura. Incluye integración con Google Sheets y Drive, generación de PDF y panel de KPIs.

## Funcionalidades

- Registro de vehículos con datos del cliente, placa, seguro, etc.
- Control por fases: reparación, pintura, inspección, etc.
- Subida de fotos/videos a Google Drive (con estructura automática)
- Generación de PDF por unidad
- Dashboard de indicadores (KPIs)
- Alertas por correo desde tu cuenta Gmail

## Requisitos
Ver `requirements.txt`
