import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="HMI Prácticas Henkel", layout="centered")

# --- CONEXIÓN A GOOGLE SHEETS ---
# Este es el código que el mensaje te pedía verificar
conn = st.connection("gsheets", type=GSheetsConnection)

# Leer datos existentes del Excel
df_existente = conn.read(ttl=0) 

if 'asistencias' not in st.session_state:
    st.session_state.asistencias = df_existente['asistencia'].tolist() if not df_existente.empty else []

# --- CONFIGURACIÓN ---
st.title("📊 HMI Control de Prácticas")
HORAS_DIARIAS = {"Lunes": 10, "Martes": 5, "Miércoles": 5, "Viernes": 5}
META = 320

# Calcular horas
total_hrs = sum(HORAS_DIARIAS.get(reg.split(" - ")[1], 0) for reg in st.session_state.asistencias)

# --- DASHBOARD ---
col1, col2 = st.columns(2)
col1.metric("Horas Acumuladas", f"{total_hrs} hrs")
col2.metric("Meta Restante", f"{max(0, META - total_hrs)} hrs")
st.progress(min(total_hrs / META, 1.0))

# --- REGISTRO ---
st.subheader("🗓️ Marcado de Asistencia")
for s in range(1, 17):
    with st.expander(f"SEMANA {s}"):
        for dia, hrs in HORAS_DIARIAS.items():
            id_tag = f"Semana {s} - {dia}"
            esta_marcado = id_tag in st.session_state.asistencias
            
            if st.checkbox(f"{dia} ({hrs} hrs)", value=esta_marcado, key=id_tag):
                if id_tag not in st.session_state.asistencias:
                    st.session_state.asistencias.append(id_tag)
            else:
                if id_tag in st.session_state.asistencias:
                    st.session_state.asistencias.remove(id_tag)

# --- BOTÓN DE GUARDADO ---
if st.button("💾 SINCRONIZAR CON LA NUBE", type="primary", use_container_width=True):
    nuevo_df = pd.DataFrame({"asistencia": st.session_state.asistencias})
    conn.update(data=nuevo_df)
    st.success("¡Datos guardados en Google Sheets!")
    st.balloons()
