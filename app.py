
import pandas as pd
import numpy as np
import streamlit as st

st.set_page_config(page_title="KinoLab AI - Multi-Premio", page_icon="🎯", layout="wide")

st.title("🎯 KinoLab AI: Panel Multi-Premio (Kino, ReKino, Chao Jefe, etc.)")
st.markdown("Ingresa los resultados de las diferentes categorías del sorteo para actualizar el laboratorio en tiempo real.")

st.sidebar.header("📁 Base de Datos")
uploaded_file = st.sidebar.file_uploader("Sube tu archivo Excel histórico", type=["xlsx", "csv"])

if uploaded_file is not None:
    df_kino = pd.read_excel(uploaded_file)
    st.sidebar.success(f"¡Historial cargado! Total de sorteos: {len(df_kino)}")
else:
    st.sidebar.info("Usando datos de prueba por defecto.")
    data_base = {"sorteo": [3255, 3254], "fecha": ["19/07/2026", "17/07/2026"]}
    for i in range(1, 26):
        data_base[str(i)] = np.random.choice([0, 1], size=2)
    df_kino = pd.DataFrame(data_base)

st.markdown("---")
st.subheader("✍️ Registro Manual de Sorteos Múltiples (Kino, ReKino, Chao Jefe, etc.)")

col1, col2 = st.columns(2)
with col1:
    sorteo_id = st.number_input("Número de Sorteo General", min_value=3256, value=3256, step=1)
with col2:
    fecha_sorteo = st.text_input("Fecha del Sorteo", value="22/07/2026")

# Selector de categoría o premio
categoria = st.selectbox(
    "Selecciona la categoría del premio a ingresar:",
    [
        "1. Kino Principal (14 aciertos)",
        "2. ReKino",
        "3. RequeteKino",
        "4. Chao Jefe $2 Millones",
        "5. Chao Jefe $3 Millones",
        "6. Súper Combo Marraqueta"
    ]
)

numeros_input = st.text_input(
    "Ingresa los números ganadores de esta categoría (separados por comas o guiones)",
    "01, 02, 05, 08, 09, 11, 13, 14, 16, 18, 20, 22, 24, 25"
)

if st.button("🚀 Registrar Categoría y Actualizar IA"):
    try:
        nums = [int(n.strip()) for n in numeros_input.replace("-", ",").split(",")]
        if len(nums) < 10 or len(nums) > 15:
            st.warning("⚠️ Asegúrate de ingresar una combinación válida para la categoría seleccionada.")
        else:
            st.success(f"¡Categoría '{categoria}' registrada con éxito para el Sorteo {sorteo_id}!")
            
            # Simulación de recálculo del ranking considerando esta nueva categoría
            ranking = []
            for num in range(1, 26):
                prob = np.random.uniform(0.45, 0.70)
                if num in nums:
                    prob += 0.20 # Mayor peso si salió en esta categoría
                ranking.append({"Número": num, "Probabilidad Ponderada": round(prob, 4)})
            
            df_res = pd.DataFrame(ranking).sort_values(by="Probabilidad Ponderada", ascending=False)
            
            st.markdown(f"### 📊 Ranking Actualizado tras registrar: *{categoria}*")
            st.dataframe(df_res, use_container_width=True)
            
            mejor_comb = sorted(df_res.head(14)["Número"].tolist())
            st.markdown("### 🏆 Combinación Óptima General Sugerida (Top 14):")
            st.success(f"{mejor_comb}")
            
    except Exception as e:
        st.error(f"Error al procesar los números. Revisa el formato: {e}")
