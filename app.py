import streamlit as st
import pandas as pd

st.set_page_config(page_title="Pesquisa de Itens", layout="centered")
st.title("🔍 Pesquisa de Itens")

# Lê o arquivo que já está no repositório
try:
    df_base = pd.read_excel("Pesquisa de itens.xlsm", engine="openpyxl")

    # Normaliza nomes das colunas
    df_base.columns = df_base.columns.str.strip().str.upper()

    # Verifica se colunas essenciais existem
    if "CÓDIGO" in df_base.columns and "DESCRIÇÃO" in df_base.columns:
        termo_busca = st.text_input("Digite o termo ou código que deseja buscar:")

        if termo_busca:
            termos = termo_busca.strip().upper().split()

            filtro = df_base.apply(
                lambda row: any(
                    termo in str(row["CÓDIGO"]).upper() or termo in str(row["DESCRIÇÃO"]).upper()
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
    else:
        st.error("❌ As colunas 'CÓDIGO' e 'DESCRIÇÃO' não foram encontradas.")
except Exception as e:
    st.error("❌ Erro ao carregar a base de dados:")
    st.code(str(e))
