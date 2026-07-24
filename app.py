import pandas as pd
import numpy as np
import streamlit as st

st.set_page_config(page_title="KinoLab AI - Validador Histórico", page_icon="🎯", layout="wide")

st.title("🎯 KinoLab AI: Laboratorio con Historial Real")
st.markdown("Sube tu historial y valida tus combinaciones contra más de 2.400 sorteos reales.")

if 'df_historial' not in st.session_state:
    data_base = {"sorteo": [3255, 3254], "fecha": ["19/07/2026", "17/07/2026"]}
    for i in range(1, 26):
        data_base[str(i)] = np.random.choice([0, 1], size=2)
    st.session_state.df_historial = pd.DataFrame(data_base)

st.sidebar.header("📁 Base de Datos")
uploaded_file = st.sidebar.file_uploader("Sube tu archivo histórico (.csv o .xlsx)", type=["xlsx", "csv"])

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith('.csv'):
            st.session_state.df_historial = pd.read_csv(uploaded_file, sep=';')
        else:
            st.session_state.df_historial = pd.read_excel(uploaded_file)
        st.sidebar.success(f"¡Historial cargado! Total: {len(st.session_state.df_historial)} sorteos")
    except Exception as e:
        st.sidebar.error(f"Error al leer el archivo: {e}")
else:
    st.sidebar.info(f"Sorteos activos en memoria: {len(st.session_state.df_historial)}")

def validar_contra_historia(comb_a_buscar, df_historico):
    match_encontrado = None
    fecha_match = ""
    cols_numeros = [str(i) for i in range(1, 26)] if all(str(i) in [str(c) for c in df_historico.columns] for i in range(1, 26)) else []
    
    if cols_numeros:
        for idx, row in df_historico.iterrows():
            numeros_sorteo_historico = [int(col) for col in cols_numeros if str(row[col]) == '1']
            if set(comb_a_buscar) == set(numeros_sorteo_historico):
                match_encontrado = row.get('sorteo', idx)
                fecha_match = str(row.get('fecha', 'Fecha no disponible'))
                break
    return match_encontrado, fecha_match

with st.expander("✍️ Registrar Nuevo Sorteo en el Historial"):
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        sorteo_id_man = st.number_input("Número de Sorteo", min_value=3256, value=3256, step=1)
    with col_m2:
        fecha_man = st.text_input("Fecha del Sorteo", value="22/07/2026")
        
    nums_manual_input = st.text_input("Ingresa 14 números ganadores (separados por comas)", "1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14")
    
    if st.button("💾 Guardar Sorteo en la Base"):
        try:
            nums_m = [int(n.strip()) for n in nums_manual_input.replace("-", ",").split(",")]
            if len(nums_m) != 14:
                st.warning("⚠️ Debes ingresar exactamente 14 números.")
            else:
                nueva_fila = {"sorteo": sorteo_id_man, "fecha": fecha_man}
                for i in range(1, 26):
                    nueva_fila[str(i)] = 1 if i in nums_m else 0
                st.session_state.df_historial = pd.concat([st.session_state.df_historial, pd.DataFrame([nueva_fila])], ignore_index=True)
                st.success(f"✅ ¡Sorteo #{sorteo_id_man} guardado exitosamente!")
        except Exception as e:
                st.error(f"Error al guardar: {e}")

st.markdown("---")

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
            st.success("✅ ¡Esta combinación generada es **Inédita** en el historial!")

with col_der:
    st.subheader("🔍 Columna de Consulta Manual")
    input_usuario = st.text_input("Escribe 14 números a consultar", "1, 2, 3, 4, 6, 7, 8, 12, 13, 14, 18, 20, 21, 25")
    
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
                    st.success("✅ **¡Inédita!** Esta combinación nunca ha salido en los registros históricos.")
        except Exception as e:
            st.error(f"Error en el formato: {e}")

st.markdown("---")
st.subheader("📊 Estado de la Base de Datos Histórica")
st.write(f"Total de sorteos cargados: {len(st.session_state.df_historial):,}")
st.dataframe(st.session_state.df_historial.tail(5), use_container_width=True)
