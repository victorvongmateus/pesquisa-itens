import streamlit as st
import pandas as pd
from PIL import Image

st.set_page_config(page_title="Pesquisa de Itens", layout="wide")

# Layout superior: logo à esquerda, título e nome à direita
col1, col2 = st.columns([1, 4])

with col1:
    try:
        logo = Image.open("logo_aroeira.png")
        st.image(logo, width=120)
    except:
        st.write("Logo não encontrada")

with col2:
    st.markdown(
        """
        <div style="display: flex; flex-direction: column; justify-content: center;">
            <h1 style="margin-bottom: 0;">Pesquisa de Itens – Bioenergética Aroeira</h1>
            <p style="font-weight: bold; font-size: 16px; margin-top: 5px;">
                Desenvolvido por Victor von Glehn Mateus
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

# Leitura da base de dados
df_base = pd.read_excel("Pesquisa de itens.xlsm", engine="openpyxl")
df_base.columns = df_base.columns.str.strip().str.upper()

# Campo de busca
termo_busca = st.text_input("Digite o termo ou código que deseja buscar:")

if termo_busca:
    termos = termo_busca.strip().upper().split()

    # Aplica filtro
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
        st.dataframe(resultados.reset_index(drop=True), use_container_width=True)
    else:
        st.warning("Nenhum resultado encontrado.")
