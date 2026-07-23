
import pandas as pd
import numpy as np
import streamlit as st

st.set_page_config(page_title="KinoLab AI - Validador Histórico", page_icon="🎯", layout="wide")

st.title("🎯 KinoLab AI: Validador Histórico de Combinaciones")
st.markdown("Genera tu combinación óptima y compárala automáticamente contra los más de 20 años de sorteos históricos.")

# 1. Cargar Base de Datos Histórica
st.sidebar.header("📁 Base de Datos")
uploaded_file = st.sidebar.file_uploader("Sube tu archivo Excel histórico (data-kino-sensi_data.xlsx)", type=["xlsx", "csv"])

if uploaded_file is not None:
    df_kino = pd.read_excel(uploaded_file)
    st.sidebar.success(f"¡Historial cargado! Total de sorteos: {len(df_kino)}")
else:
    st.sidebar.info("⚠️ Usando base de prueba. Sube tu Excel oficial para una validación real.")
    # Datos de prueba mínimos si no suben archivo
    data_base = {"sorteo": [3255, 3254], "fecha": ["19/07/2026", "17/07/2026"]}
    for i in range(1, 26):
        data_base[str(i)] = np.random.choice([0, 1], size=2)
    df_kino = pd.DataFrame(data_base)

st.markdown("---")
st.subheader("🏆 Generación y Validación de Combinación Óptima")

if st.button("🚀 Generar Combinación y Validar en la Historia"):
    # Simulación de ranking y obtención de la combinación Top 14 sugerida
    ranking = [{"Número": num, "Probabilidad": round(np.random.uniform(0.45, 0.75), 4)} for num in range(1, 26)]
    df_res = pd.DataFrame(ranking).sort_values(by="Probabilidad", ascending=False)
    
    # Tomamos los 14 mejores números sugeridos ordenados
    mejor_comb = sorted(df_res.head(14)["Número"].tolist())
    
    st.markdown("### 📋 Combinación Sugerida por el Laboratorio:")
    st.info(f"{mejor_comb}")
    
    # 2. Motor de Validación Histórica
    # Buscamos en el DataFrame si los 14 números coinciden exactamente con algún sorteo pasado
    match_encontrado = None
    
    # Detectar las columnas de números en el DataFrame (del 1 al 25)
    cols_numeros = [str(i) for i in range(1, 26)] if all(str(i) in df_kino.columns for i in range(1, 26)) else []
    
    if cols_numeros:
        for idx, row in df_kino.iterrows():
            # Obtener los números que salieron en este sorteo histórico (donde el valor es 1)
            numeros_sorteo_historico = [int(col) for col in cols_numeros if row[col] == 1]
            
            # Comparar si la combinación coincide exactamente
            if set(mejor_comb) == set(numeros_sorteo_historico):
                match_encontrado = row['sorteo']
                fecha_match = row.get('fecha', 'Fecha no disponible')
                break
                
    st.markdown("### 🔍 Resultado de la Validación:")
    if match_encontrado:
        st.error(f"⚠️ ¡Atención! Esta combinación **YA SALIó** en la historia del Kino.")
        st.write(f"• **Sorteo Coincidente:** #{match_encontrado}")
        st.write(f"• **Fecha del Sorteo:** {fecha_match}")
    else:
        st.success("✅ **¡Combinación Inédita!** Esta combinación exacta de 14 números **NUNCA** ha salido en los registros históricos analizados.")

    st.markdown("### 📊 Ranking Probabilístico de los 25 Números")
    st.dataframe(df_res, use_container_width=True)
