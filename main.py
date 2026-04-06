import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# 1. Configuración de la App
st.set_page_config(page_title="HMI Henkel - WAPOSAT", layout="centered")

# 2. Conexión a Google Sheets (Usando tus Secrets corregidos)
# Si aquí da error, es por los Secrets en el panel de Streamlit
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    df_existente = conn.read(ttl=0)
    
    # Extraer lista de asistencias si la columna existe
    if not df_existente.empty and 'asistencia' in df_existente.columns:
        lista_asistencias = df_existente['asistencia'].dropna().tolist()
    else:
        lista_asistencias = []
except Exception as e:
    st.warning("Conectando con la base de datos...")
    lista_asistencias = []

# 3. Estado de la sesión
if 'asistencias' not in st.session_state:
    st.session_state.asistencias = lista_asistencias

# 4. Interfaz de Usuario
st.title("📊 Control de Prácticas - Henkel")
st.write("Registra tus horas para WAPOSAT de forma segura.")

# Cálculo de horas (L:10h, M-V:5h)
HORAS_MAP = {"Lunes": 10, "Martes": 5, "Miércoles": 5, "Viernes": 5}
total_hrs = sum(HORAS_MAP.get(reg.split(" - ")[1], 0) for reg in st.session_state.asistencias)

# Métricas
c1, c2 = st.columns(2)
c1.metric("Horas Logradas", f"{total_hrs} h")
c2.metric("Meta Final", "320 h")
st.progress(min(total_hrs / 320, 1.0))

# 5. Marcado de Asistencia (Semanas 1-16)
with st.expander("📅 REGISTRAR DÍAS TRABAJADOS"):
    for s in range(1, 17):
        st.subheader(f"Semana {s}")
        cols = st.columns(4)
        for i, (dia, h) in enumerate(HORAS_MAP.items()):
            tag = f"S{s} - {dia}"
            is_checked = cols[i].checkbox(f"{dia} ({h}h)", value=(tag in st.session_state.asistencias), key=tag)
            
            if is_checked and tag not in st.session_state.asistencias:
                st.session_state.asistencias.append(tag)
            elif not is_checked and tag in st.session_state.asistencias:
                st.session_state.asistencias.remove(tag)

# 6. Botón de Guardado
if st.button("💾 GUARDAR CAMBIOS EN LA NUBE", type="primary"):
    try:
        nuevo_df = pd.DataFrame({"asistencia": st.session_state.asistencias})
        conn.update(data=nuevo_df)
        st.success("¡Datos guardados con éxito en Google Sheets!")
        st.balloons()
    except Exception as e:
        st.error(f"Error al guardar: {e}")
        st.info("Revisa que hayas compartido el Excel con el correo de la cuenta de servicio.")
