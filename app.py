import streamlit as st
import pandas as pd
from PIL import Image

st.set_page_config(page_title="Pesquisa de Itens", layout="centered")

# Logo da Aroeira
try:
    logo = Image.open("logo_aroeira.png")
    st.image(logo, width=200)
except:
    pass  # Caso o logo não exista, evita erro

# Título centralizado
st.markdown("<h1 style='text-align: center;'>🔍 Pesquisa de Itens</h1>", unsafe_allow_html=True)

# Leitura da base de dados
df_base = pd.read_excel("Pesquisa de itens.xlsm", engine="openpyxl")
df_base.columns = df_base.columns.str.strip().str.upper()  # Normaliza os nomes das colunas

# Campo de pesquisa
termo_busca = st.text_input("Digite o termo ou código que deseja buscar:")

if termo_busca:
    termos = termo_busca.strip().upper().split()

    # Aplica o filtro nas colunas CODIGO e DESCRICAO (sem acento, como estão na planilha)
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

# Rodapé com nome do desenvolvedor
st.markdown(
    """
    <div style="text-align: center; font-size: 12px; margin-top: 50px;">
        Desenvolvido por Victor von Glehn Mateus
    </div>
    """,
    unsafe_allow_html=True
)
