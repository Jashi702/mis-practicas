import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="HMI Henkel", layout="centered")

# --- CONEXIÓN ---
conn = st.connection("gsheets", type=GSheetsConnection)

# Intentar leer, si falla, crear un DataFrame vacío
try:
    df_existente = conn.read(worksheet="Sheet1", ttl=0)
    if 'asistencia' in df_existente.columns:
        lista_asistencias = df_existente['asistencia'].dropna().tolist()
    else:
        lista_asistencias = []
except Exception:
    lista_asistencias = []

if 'asistencias' not in st.session_state:
    st.session_state.asistencias = lista_asistencias

# --- INTERFAZ ---
st.title("📊 Control de Prácticas WAPOSAT")
HORAS = {"Lunes": 10, "Martes": 5, "Miércoles": 5, "Viernes": 5}
total = sum(HORAS.get(reg.split(" - ")[1], 0) for reg in st.session_state.asistencias)

col1, col2 = st.columns(2)
col1.metric("Acumuladas", f"{total} hrs")
col2.metric("Meta", "320 hrs")
st.progress(min(total / 320, 1.0))

# --- REGISTRO ---
with st.expander("📅 MARCAR ASISTENCIA"):
    for s in range(1, 17):
        st.write(f"**Semana {s}**")
        cols = st.columns(4)
        for i, (dia, h) in enumerate(HORAS.items()):
            tag = f"S{s} - {dia}"
            if cols[i].checkbox(f"{dia}", value=(tag in st.session_state.asistencias), key=tag):
                if tag not in st.session_state.asistencias:
                    st.session_state.asistencias.append(tag)
            elif tag in st.session_state.asistencias:
                st.session_state.asistencias.remove(tag)

# --- GUARDADO ---
if st.button("💾 GUARDAR EN GOOGLE CLOUD", type="primary"):
    nuevo_df = pd.DataFrame({"asistencia": st.session_state.asistencias})
    conn.update(worksheet="Sheet1", data=nuevo_df)
    st.success("¡Sincronizado con Google Sheets!")
    st.balloons()
