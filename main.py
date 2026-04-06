import streamlit as st
import pandas as pd

st.set_page_config(page_title="HMI Prácticas Henkel", layout="centered")

st.title("📊 HMI Control de Prácticas")
st.write("Registra tus 320 horas de ingeniería")

# Configuración de horas
config_h = {"Lunes": 10, "Martes": 5, "Miércoles": 5, "Viernes": 5}
meta = 320

# Inicializar historial en la memoria del navegador
if 'asistencias' not in st.session_state:
    st.session_state.asistencias = ["Semana 1 - Miércoles"]

# --- CÁLCULO DE HORAS ---
total_hrs = 0
for registro in st.session_state.asistencias:
    dia_clave = registro.split(" - ")[1]
    total_hrs += config_h.get(dia_clave, 0)

# Dashboard Visual
col1, col2 = st.columns(2)
col1.metric("Horas Acumuladas", f"{total_hrs} hrs")
col2.metric("Meta Restante", f"{max(0, meta - total_hrs)} hrs")

st.progress(min(total_hrs / meta, 1.0))

# --- REGISTRO SEMANAL ---
st.subheader("🗓️ Bitácora Semanal")

for s in range(1, 17):
    with st.expander(f"SEMANA {s}"):
        for dia, hrs in config_h.items():
            id_tag = f"Semana {s} - {dia}"
            
            # Checkbox que lee si ya estaba marcado
            is_checked = id_tag in st.session_state.asistencias
            
            if st.checkbox(f"{dia} ({hrs} hrs)", value=is_checked, key=id_tag):
                if id_tag not in st.session_state.asistencias:
                    st.session_state.asistencias.append(id_tag)
            else:
                if id_tag in st.session_state.asistencias:
                    st.session_state.asistencias.remove(id_tag)

if st.button("💾 GUARDAR AVANCE", type="primary"):
    st.success("¡Progreso actualizado correctamente!")
    st.balloons()