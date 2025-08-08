import streamlit as st
import pandas as pd
from PIL import Image

st.set_page_config(page_title="Pesquisa de Itens", layout="centered")

# Logo centralizada
try:
    logo = Image.open("logo_aroeira.png")
    st.markdown(
        """
        <div style='text-align: center;'>
            <img src='data:image/png;base64,%s' width='200'/>
        </div>
        """ % st.image(logo, output_format="PNG").image_to_bytes().decode("utf-8"),
        unsafe_allow_html=True
    )
except:
    # Fallback em caso de erro
    st.image(logo, width=200)

# Desenvolvido por (abaixo da logo)
st.markdown(
    """
    <div style="text-align: center; font-size: 16px; margin-top: -10px; margin-bottom: 30px;">
        Desenvolvido por Victor von Glehn Mateus
    </div>
    """,
    unsafe_allow_html=True
)

# Título (sem emoji/lupa)
st.markdown("<h1 style='text-align: center;'>Pesquisa de Itens</h1>", unsafe_allow_html=True)

# Carrega base
df_base = pd.read_excel("Pesquisa de itens.xlsm", engine="openpyxl")
df_base.columns = df_base.columns.str.strip().str.upper()

# Campo de busca
termo_busca = st.text_input("Digite o termo ou código que deseja buscar:")

if termo_busca:
    termos = termo_busca.strip().upper().split()

    filtro = df_base.apply(
        lambda row: any(
            termo in str(row.get("CODIGO", "")).upper() or termo in str(row.get("DESCRICAO", "")).upper()
            for termo in termos
        ),
        axis=1
    )

    resultados = df_base[filtro]

    if not resultados.empty:
        st.success(f"{len(resultados)} item(ns) encontrado(s).")
        st.dataframe(resultados)
    else:
        st.warning("Nenhum resultado encontrado.")
