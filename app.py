from pathlib import Path
import streamlit as st
import pandas as pd

# Caminho e nome da planilha
ARQUIVO = "Pesquisa de itens.xlsm"
ABA = "Base"

st.set_page_config(page_title="Pesquisa de Itens", layout="wide")

# Frase de autoria no topo
st.markdown(
    "<p style='text-align:center; font-size:16px; color:gray;'>"
    "Desenvolvido por Victor von Glehn - Especialista de Engenharia Agrícola"
    "</p>",
    unsafe_allow_html=True
)

# Título principal
st.markdown("<h1 style='text-align:center;'>🔍 Pesquisa de Itens - Bioenergética Aroeira</h1>", unsafe_allow_html=True)

# Entrada de texto
entrada = st.text_area("Digite os códigos ou palavras separadas por vírgula ou enter:", height=70)

# Botão de busca
if st.button("Buscar"):
    try:
        # Lê a planilha com os nomes de colunas como estão
        df = pd.read_excel(ARQUIVO, sheet_name=ABA)

        # Copia para uma versão que será usada na busca (em minúsculas)
        df_busca = df.astype(str).apply(lambda x: x.str.lower())

        # Extrai os termos digitados
        termos = [t.strip().lower() for t in entrada.replace("\n", ",").split(",") if t.strip() != ""]

        # Filtra os resultados com base em qualquer coluna
        resultados = df[df_busca.apply(lambda row: any(t in " ".join(row.values) for t in termos), axis=1)]

        # Exibe a tabela sem índice e com nome original das colunas
        if not resultados.empty:
            st.success(f"{len(resultados)} item(ns) encontrado(s).")
            st.dataframe(resultados.reset_index(drop=True), use_container_width=True)
        else:
            st.warning("Nenhum item encontrado.")

    except Exception as e:
        st.error(f"Ocorreu um erro: {e}")
