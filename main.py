import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# 1. Configuración de la App
st.set_page_config(page_title="HMI Henkel - WAPOSAT", layout="centered")

# 2. Conexión Directa
conn = st.connection("gsheets", type=GSheetsConnection)

# 3. Lectura de Datos Segura
try:
    # Leemos la hoja completa
    df_existente = conn.read(ttl=0)
    if not df_existente.empty and 'asistencia' in df_existente.columns:
        lista_asistencias = df_existente['asistencia'].dropna().tolist()
    else:
        lista_asistencias = []
except Exception:
    lista_asistencias = []

# 4. Estado de la sesión
if 'asistencias' not in st.session_state:
    st.session_state.asistencias = lista_asistencias

# 5. Interfaz de Usuario
st.title("📊 Control de Prácticas - Henkel")
st.write("Registra tus avances para WAPOSAT SAC")

HORAS_MAP = {"Lunes": 10, "Martes": 5, "Miércoles": 5, "Viernes": 5}
total_hrs = sum(HORAS_MAP.get(reg.split(" - ")[1], 0) for reg in st.session_state.asistencias)

c1, c2 = st.columns(2)
c1.metric("Horas Logradas", f"{total_hrs} h")
c2.metric("Meta Final", "320 h")
st.progress(min(total_hrs / 320, 1.0))

with st.expander("📅 REGISTRAR DÍAS TRABAJADOS", expanded=True):
    for s in range(1, 17):
        st.subheader(f"Semana {s}")
        cols = st.columns(4)
        for i, (dia, h) in enumerate(HORAS_MAP.items()):
            tag = f"S{s} - {dia}"
            is_checked = cols[i].checkbox(f"{dia}", value=(tag in st.session_state.asistencias), key=tag)
            if is_checked and tag not in st.session_state.asistencias:
                st.session_state.asistencias.append(tag)
            elif not is_checked and tag in st.session_state.asistencias:
                st.session_state.asistencias.remove(tag)

# 6. BOTÓN DE GUARDADO REFORMULADO
if st.button("💾 GUARDAR EN GOOGLE CLOUD", type="primary"):
    if not st.session_state.asistencias:
        st.warning("No hay días seleccionados para guardar.")
    else:
        try:
            # Preparamos el DataFrame
            nuevo_df = pd.DataFrame({"asistencia": st.session_state.asistencias})
            
            # EL CAMBIO CLAVE: Usamos clear_cache antes de actualizar
            st.cache_data.clear()
            
            # Actualizamos indicando que use la primera hoja
            conn.update(data=nuevo_df)
            
            st.success("¡Sincronización exitosa con el Excel!")
            st.balloons()
        except Exception as e:
            st.error(f"Error técnico: {e}")
            st.info("Intenta borrar los datos manualmente en el Excel y dale a guardar de nuevo.")
