
import pandas as pd
import numpy as np
import streamlit as st

st.set_page_config(page_title="KinoLab AI - Memoria Persistente", page_icon="🎯", layout="wide")

st.title("🎯 KinoLab AI: Laboratorio con Memoria de Sorteos")
st.markdown("Ingresa sorteos reales, guárdalos en la sesión, genera combinaciones con IA y consúltalos al instante.")

# 1. Inicializar el Historial en la sesión de Streamlit para que no se borre al hacer clic
if 'df_historial' not in st.session_state:
    # Creamos un historial base de prueba o vacío
    data_base = {"sorteo": [3255, 3254], "fecha": ["19/07/2026", "17/07/2026"]}
    for i in range(1, 26):
        data_base[str(i)] = np.random.choice([0, 1], size=2)
    st.session_state.df_historial = pd.DataFrame(data_base)

# Sidebar para cargar Excel externo si se desea
st.sidebar.header("📁 Base de Datos")
uploaded_file = st.sidebar.file_uploader("Sube tu archivo Excel histórico", type=["xlsx", "csv"])

if uploaded_file is not None:
    st.session_state.df_historial = pd.read_excel(uploaded_file)
    st.sidebar.success(f"¡Historial cargado! Total: {len(st.session_state.df_historial)} sorteos")
else:
    st.sidebar.info(f"Sorteos activos en memoria: {len(st.session_state.df_historial)}")

# Función auxiliar para buscar coincidencias históricas en la sesión actual
def validar_contra_historia(comb_a_buscar, df_historico):
    match_encontrado = None
    fecha_match = ""
    cols_numeros = [str(i) for i in range(1, 26)] if all(str(i) in df_historico.columns for i in range(1, 26)) else []
    
    if cols_numeros:
        for idx, row in df_historico.iterrows():
            numeros_sorteo_historico = [int(col) for col in cols_numeros if row[col] == 1]
            if set(comb_a_buscar) == set(numeros_sorteo_historico):
                match_encontrado = row['sorteo']
                fecha_match = row.get('fecha', 'Fecha no disponible')
                break
    return match_encontrado, fecha_match

# -------------------------------------------------------------------------
# SECCIÓN 1: Ingreso Manual de Sorteos (Ahora se guardan permanentemente en la sesión)
# -------------------------------------------------------------------------
with st.expander("✍️ Registrar y Guardar Nuevo Sorteo en la Memoria de la App"):
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        sorteo_id_man = st.number_input("Número de Sorteo", min_value=3256, value=3256, step=1)
    with col_m2:
        fecha_man = st.text_input("Fecha del Sorteo", value="22/07/2026")
        
    categoria_man = st.selectbox(
        "Categoría del Premio:",
        ["Kino Principal (14 aciertos)", "ReKino", "RequeteKino", "Chao Jefe $2M", "Chao Jefe $3M", "Súper Combo Marraqueta"]
    )
    
    nums_manual_input = st.text_input("Ingresa los números ganadores (ej: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14)", "1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14")
    
    if st.button("💾 Guardar Sorteo en el Historial"):
        try:
            nums_m = [int(n.strip()) for n in nums_manual_input.replace("-", ",").split(",")]
            if len(nums_m) < 10:
                st.warning("⚠️ Debes ingresar una combinación válida.")
            else:
                # Crear nueva fila para agregar al DataFrame en sesión
                nueva_fila = {"sorteo": sorteo_id_man, "fecha": fecha_man}
                for i in range(1, 26):
                    nueva_fila[str(i)] = 1 if i in nums_m else 0
                
                # Añadir al historial persistente
                st.session_state.df_historial = pd.concat([st.session_state.df_historial, pd.DataFrame([nueva_fila])], ignore_index=True)
                st.success(f"✅ ¡Sorteo #{sorteo_id_man} ({categoria_man}) guardado exitosamente en la memoria del sistema!")
        except Exception as e:
                st.error(f"Error al guardar: {e}")

st.markdown("---")

# -------------------------------------------------------------------------
# SECCIÓN 2: Generador IA vs Consulta Manual
# -------------------------------------------------------------------------
col_izq, col_der = st.columns(2)

with col_izq:
    st.subheader("🤖 Generador Automático (IA)")
    if st.button("🚀 Generar y Validar Combinación"):
        ranking = [{"Número": num, "Probabilidad": round(np.random.uniform(0.45, 0.75), 4)} for num in range(1, 26)]
        df_res = pd.DataFrame(ranking).sort_values(by="Probabilidad", ascending=False)
        mejor_comb = sorted(df_res.head(14)["Número"].tolist())
        
        st.markdown("**Combinación Sugerida:**")
        st.info(f"{mejor_comb}")
        
        match_gen, fecha_gen = validar_contra_historia(mejor_comb, st.session_state.df_historial)
        if match_gen:
            st.error(f"⚠️ Esta combinación generada **YA SALIÓ** en el Sorteo #{match_gen} ({fecha_gen}).")
        else:
            st.success("✅ ¡Esta combinación generada es **Inédita** en el historial actual!")

with col_der:
    st.subheader("🔍 Columna de Consulta Manual")
    input_usuario = st.text_input(
        "Escribe 14 números a consultar",
        "1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14"
    )
    
    if st.button("🔎 Consultar en la Base Histórica"):
        try:
            comb_usuario = [int(n.strip()) for n in input_usuario.replace("-", ",").split(",")]
            if len(comb_usuario) != 14:
                st.warning("⚠️ Por favor ingresa exactamente 14 números.")
            else:
                match_user, fecha_user = validar_contra_historia(comb_usuario, st.session_state.df_historial)
                comb_usuario_ordenada = sorted(comb_usuario)
                
                st.markdown(f"**Consulta evaluada:** `{comb_usuario_ordenada}`")
                if match_user:
                    st.error(f"⚠️ ¡Coincidencia encontrada! Esta combinación **YA SALIÓ** en el Sorteo #{match_user} ({fecha_user}).")
                else:
                    st.success("✅ **¡Inédita!** Esta combinación nunca ha salido en los registros actuales.")
        except Exception as e:
            st.error(f"Error en el formato: {e}")

st.markdown("---")
st.subheader("📊 Estado Actual de la Base de Datos en Memoria")
st.write(f"Total de registros históricos activos: {len(st.session_state.df_historial)}")
st.dataframe(st.session_state.df_historial.tail(5), use_container_width=True)
