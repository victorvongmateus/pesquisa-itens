from pathlib import Path
import streamlit as st
import pandas as pd

# Caminho para o arquivo Excel
ARQUIVO = "Pesquisa de itens.xlsm"
ABA = "Base"

st.set_page_config(page_title="Pesquisa de Itens", layout="wide")

# Frase de autoria
st.markdown(
    "<p style='text-align:center; font-size:16px; color:gray;'>"
    "Desenvolvido por Victor von Glehn - Especialista de Engenharia Agrícola"
    "</p>",
    unsafe_allow_html=True
)

# Título da aplicação
st.markdown("<h1 style='text-align:center;'>🔍 Pesquisa de Itens - Bioenergética Aroeira</h1>", unsafe_allow_html=True)

# Campo de entrada
entrada = st.text_area("Digite os códigos ou palavras separadas por vírgula ou enter:", height=70)

# Botão de busca
if st.button("Buscar"):
    try:
        # Carrega a planilha
        df = pd.read_excel(ARQUIVO, sheet_name=ABA)

        # Garante que todas as colunas estejam com nomes minúsculos sem espaços
        df.columns = [col.strip().lower() for col in df.columns]

        # Converte tudo para string e minúscula para facilitar a busca
        df = df.astype(str).apply(lambda x: x.str.lower())

        # Separa os termos de busca
        termos = [t.strip().lower() for t in entrada.replace("\n", ",").split(",") if t.strip() != ""]

        # Filtra os resultados
        resultados = df[df.apply(lambda row: any(t in " ".join(row.values) for t in termos), axis=1)]

        # Exibe os resultados sem o índice
        if not resultados.empty:
            st.success(f"{len(resultados)} item(ns) encontrado(s).")
            st.dataframe(resultados.reset_index(drop=True), use_container_width=True)
        else:
            st.warning("Nenhum item encontrado.")

    except Exception as e:
        st.error(f"Ocorreu um erro: {e}")
