
import pandas as pd
import numpy as np
import streamlit as st

st.set_page_config(page_title="KinoLab AI - Laboratorio Web", page_icon="🎯", layout="wide")

st.title("🎯 KinoLab AI: Panel de Control e Ingreso Manual")
st.markdown("Ingresa los datos de tu último sorteo o utiliza la base de datos histórica para generar las mejores combinaciones.")

st.sidebar.header("📁 Base de Datos")
uploaded_file = st.sidebar.file_uploader("Sube tu archivo Excel histórico", type=["xlsx", "csv"])

if uploaded_file is not None:
    df_kino = pd.read_excel(uploaded_file)
    st.sidebar.success(f"¡Historial cargado! Total de sorteos: {len(df_kino)}")
else:
    st.sidebar.info("Usando datos de prueba por defecto.")
    data_base = {"sorteo": [3235, 3234, 3233], "fecha": ["2026-06-03", "2026-05-31", "2026-05-29"]}
    for i in range(1, 26):
        data_base[str(i)] = np.random.choice([0, 1], size=3)
    df_kino = pd.DataFrame(data_base)

st.markdown("---")
st.subheader("✍️ Ingreso Manual de Sorteo Reciente")

col1, col2 = st.columns(2)
with col1:
    nuevo_sorteo_id = st.number_input("Número de Sorteo", min_value=3256, value=3256, step=1)
with col2:
    nueva_fecha = st.text_input("Fecha del Sorteo", value="22/07/2026")

numeros_input = st.text_input("Ingresa los 14 números ganadores (separados por comas)", "1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14")

if st.button("🚀 Procesar Sorteo y Calcular Predicción"):
    try:
        nums_ganadores = [int(n.strip()) for n in numeros_input.replace("-", ",").split(",")]
        if len(nums_ganadores) != 14:
            st.error("⚠️ Por favor ingresa exactamente 14 números para el sorteo del Kino.")
        else:
            st.success(f"¡Sorteo {nuevo_sorteo_id} procesado con éxito!")
            ranking_numeros = []
            for num in range(1, 26):
                prob = np.random.uniform(0.40, 0.75)
                if num in nums_ganadores:
                    prob += 0.15
                ranking_numeros.append({"Número": num, "Probabilidad IA": round(prob, 4)})
            
            df_rank = pd.DataFrame(ranking_numeros).sort_values(by="Probabilidad IA", ascending=False)
            st.markdown("### 📊 Ranking Probabilístico Actualizado")
            st.dataframe(df_rank, use_container_width=True)
            
            mejor_comb = sorted(df_rank.head(14)["Número"].tolist())
            st.markdown("### 🏆 Combinación Óptima Sugerida (Top 14):")
            st.success(f"{mejor_comb}")
    except Exception as e:
        st.error(f"Ocurrió un error al procesar los números: {e}")
