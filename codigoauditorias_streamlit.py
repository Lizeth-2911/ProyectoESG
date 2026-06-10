# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 23:01:43 2026

@author: unik0
"""
import streamlit as st
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import pandas as pd

# --- 1. Leer credenciales desde Secrets ---
credenciales = st.secrets["credenciales"]
token = st.secrets["token"]

# --- 2. Construir objeto Credentials ---
creds = Credentials(
    token=token["token"],
    refresh_token=token["refresh_token"],
    token_uri=token["token_uri"],
    client_id=token["client_id"],
    client_secret=token["client_secret"],
    scopes=[token["scope"]],
)

# --- 3. Conectar con Google Drive y Sheets ---
drive_service = build("drive", "v3", credentials=creds)
sheets_service = build("sheets", "v4", credentials=creds)

# --- 4. IDs de tus documentos ---
MATRIZ_MAESTRA_ID = "1XyUbfYOzUhxKXIIoTYE725ung8wq7jg8Ae5FB-BT57s"
CLIENTE_EXCEL_ID = "1KR5pC6U1Mp5mymIfTS09vXQeObH5McuqrYerNsKBZSw"
CARPETA_ENTREGA_ID = "1VPOd4FhIB1reSuR1IMdRvGVf7D3jrko8"

# --- 5. Función para leer una hoja de cálculo ---
def leer_google_sheet(sheet_id, rango="Hoja1!A1:Z100"):
    result = sheets_service.spreadsheets().values().get(
        spreadsheetId=sheet_id,
        range=rango
    ).execute()
    values = result.get("values", [])
    if not values:
        return pd.DataFrame()
    return pd.DataFrame(values[1:], columns=values[0])

# --- 6. Mostrar datos en Streamlit ---
st.title("Auditoría ESG - Cliente")
st.write("Cliente: Salón de belleza express")

# Leer Matriz Maestra
st.subheader("Matriz Maestra ESG")
df_maestra = leer_google_sheet(MATRIZ_MAESTRA_ID)
st.dataframe(df_maestra)

# Leer Excel del Cliente
st.subheader("Excel del Cliente")
df_cliente = leer_google_sheet(CLIENTE_EXCEL_ID)
st.dataframe(df_cliente)

# --- 7. Subida de recibo de luz ---
st.subheader("Sube tu recibo de luz en PDF")
archivo_pdf = st.file_uploader("Selecciona tu recibo en PDF", type=["pdf"])
if archivo_pdf is not None:
    st.success(f"Archivo recibido: {archivo_pdf.name}")
    # Aquí podrías procesar el PDF con pdfplumber si lo necesitas
