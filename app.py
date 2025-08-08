import streamlit as st
import pandas as pd

st.set_page_config(page_title="Pesquisa de Itens", layout="centered")

# Logo centralizada
st.markdown(
    """
    <div style="text-align: center;">
        <img src="logo_aroeira.png" width="200"/>
    </div>
    """,
    unsafe_allow_html=True
)

# Título centralizado
st.markdown("<h1 style='text-align: center;'>🔍 Pesquisa de Itens</h1>", unsafe_allow_html=True)

# Lê a planilha salva no repositório
df_base = pd.read_excel("Pesquisa de itens.xlsm", engine="openpyxl")
df_base.columns = df_base.columns.str.strip().str.upper()

# Campo de busca
termo_busca = st.text_input("Digite o termo ou código que deseja buscar:")

if termo_busca:
    termos = termo_busca.strip().upper().split()

    filtro = df_base.apply(
        lambda row: any(
            termo in str(row.get("CÓDIGO", "")).upper() or termo in str(row.get("DESCRIÇÃO", "")).upper()
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
