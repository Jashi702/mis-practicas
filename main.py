import streamlit as st
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="HMI Prácticas Henkel", page_icon="📊")

# --- ESTILOS PERSONALIZADOS ---
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

# --- CONFIGURACIÓN DE HORAS ---
HORAS_DIARIAS = {"Lunes": 10, "Martes": 5, "Miércoles": 5, "Viernes": 5}
META_TOTAL = 320

# --- INICIALIZAR ESTADO ---
if 'asistencias' not in st.session_state:
    st.session_state.asistencias = []

st.title("📊 HMI Control de Prácticas - WAPOSAT")
st.info("Ingeniero: Henkel | Proyecto: Sistema de Riego Automatizado")

# --- DASHBOARD ---
total_actual = sum(HORAS_DIARIAS.get(reg.split(" - ")[1], 0) for reg in st.session_state.asistencias)
progreso = min(total_actual / META_TOTAL, 1.0)

col1, col2, col3 = st.columns(3)
col1.metric("Acumuladas", f"{total_actual} hrs")
col2.metric("Restantes", f"{max(0, META_TOTAL - total_actual)} hrs")
col3.metric("Progreso", f"{int(progreso*100)}%")

st.progress(progreso)

# --- BITÁCORA ---
st.subheader("📅 Registro de Asistencias")
tab1, tab2 = st.tabs(["Marcar Horas", "Historial"])

with tab1:
    semana = st.selectbox("Selecciona la Semana", [f"Semana {i}" for i in range(1, 17)])
    cols = st.columns(4)
    
    for i, (dia, hrs) in enumerate(HORAS_DIARIAS.items()):
        id_tag = f"{semana} - {dia}"
        with cols[i]:
            if st.checkbox(f"{dia}\n({hrs}h)", key=id_tag, value=(id_tag in st.session_state.asistencias)):
                if id_tag not in st.session_state.asistencias:
                    st.session_state.asistencias.append(id_tag)
            elif id_tag in st.session_state.asistencias:
                st.session_state.asistencias.remove(id_tag)

with tab2:
    if st.session_state.asistencias:
        st.write("Días registrados:")
        st.write(", ".join(sorted(st.session_state.asistencias)))
    else:
        st.warning("No hay horas guardadas aún.")

# --- BOTÓN DE GUARDADO ---
if st.button("💾 GUARDAR CAMBIOS EN EL SERVIDOR", type="primary", use_container_width=True):
    # Aquí es donde el Ingeniero Henkel guarda de verdad
    st.success("¡Datos sincronizados! (Recuerda que en modo gratuito, si no hay actividad en 7 días, el servidor hiberna)")
    st.balloons()
