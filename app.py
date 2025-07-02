import streamlit as st
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import gspread
import datetime
import os

# Configura la página
st.set_page_config(page_title="Seguimiento de Taller", layout="wide")
st.title("📋 Seguimiento de Vehículos en Taller")

# 🔐 Autenticación OAuth
flow = Flow.from_client_config(
    {
        "web": {
            "client_id": st.secrets["google_oauth"]["client_id"],
            "client_secret": st.secrets["google_oauth"]["client_secret"],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "redirect_uris": ["http://localhost:8501/", "https://<tu-app>.streamlit.app/"]
        }
    },
    scopes=[
        "https://www.googleapis.com/auth/drive",
        "https://www.googleapis.com/auth/spreadsheets"
    ],
    redirect_uri="http://localhost:8501/"
)

if "credentials" not in st.session_state:
    auth_url, _ = flow.authorization_url(prompt='consent')
    st.markdown(f"[🔐 Autoriza aquí con Google]({auth_url})")
    st.stop()
else:
    from google.oauth2.credentials import Credentials
    creds = Credentials(**st.session_state["credentials"])

# 🔧 FUNCIONES

def crear_o_obtener_carpeta(service, nombre_carpeta, id_padre):
    query = f"name = '{nombre_carpeta}' and mimeType = 'application/vnd.google-apps.folder' and '{id_padre}' in parents and trashed = false"
    respuesta = service.files().list(q=query, spaces='drive', fields='files(id, name)').execute()
    archivos = respuesta.get('files', [])
    if archivos:
        return archivos[0]['id']
    metadata = {
        'name': nombre_carpeta,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [id_padre]
    }
    carpeta = service.files().create(body=metadata, fields='id').execute()
    return carpeta['id']

def subir_archivo_a_drive(service, archivo_local, nombre_archivo, id_carpeta):
    media = MediaFileUpload(archivo_local, resumable=True)
    metadata = {
        'name': nombre_archivo,
        'parents': [id_carpeta]
    }
    archivo_subido = service.files().create(body=metadata, media_body=media, fields='id').execute()
    st.write(f"✅ Archivo subido: {nombre_archivo}")
    return archivo_subido['id']

# 📋 FORMULARIO

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
    st.markdown("### 📷 Subir archivos")
    fotos = st.file_uploader("Subir fotos del daño", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
    videos = st.file_uploader("Subir videos del inventario", type=["mp4", "mov", "avi"], accept_multiple_files=True)

    submitted = st.form_submit_button("Registrar unidad")

    if submitted:
        try:
            # Google Sheets
            gc = gspread.authorize(creds)
            sheet = gc.open_by_url("https://docs.google.com/spreadsheets/d/1rCYR_jhWeqEQVY5N4e_Aeje-6oop310PquvqPYKB9NE")
            worksheet = sheet.worksheet("Registro")

            nueva_fila = [
                datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                cliente, placa, marca, modelo, compania,
                str(fecha_ingreso), aprobado_cliente, aprobado_seguro,
                str(fecha_aprob_cliente), str(fecha_aprob_seguro),
                str(fecha_entrega_estimada), comentario
            ]
            worksheet.append_row(nueva_fila)

            # Google Drive
            drive_service = build('drive', 'v3', credentials=creds)
            ID_CARPETA_TALLER = "1YhG765mZo-o0ac1EJ34XKU_Es7z1FJqC"
            carpeta_placa_id = crear_o_obtener_carpeta(drive_service, placa, ID_CARPETA_TALLER)
            carpeta_fotos_id = crear_o_obtener_carpeta(drive_service, "Fotos", carpeta_placa_id)
            carpeta_videos_id = crear_o_obtener_carpeta(drive_service, "Videos", carpeta_placa_id)

            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

            for foto in fotos:
                nombre_temp = f"{timestamp}_{foto.name}"
                with open(nombre_temp, "wb") as f:
                    f.write(foto.getbuffer())
                subir_archivo_a_drive(drive_service, nombre_temp, nombre_temp, carpeta_fotos_id)
                os.remove(nombre_temp)

            for video in videos:
                nombre_temp = f"{timestamp}_{video.name}"
                with open(nombre_temp, "wb") as f:
                    f.write(video.getbuffer())
                subir_archivo_a_drive(drive_service, nombre_temp, nombre_temp, carpeta_videos_id)
                os.remove(nombre_temp)

            st.success(f"✅ Unidad con placa **{placa}** registrada y archivos subidos correctamente.")

        except Exception as e:
            st.error(f"❌ Error durante el registro: {e}")
