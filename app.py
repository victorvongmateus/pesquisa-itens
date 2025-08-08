import streamlit as st
import pandas as pd

# Título e campo de busca
st.set_page_config(page_title="Pesquisa de Itens", layout="centered")
st.title("Pesquisa de Itens")

# Upload do arquivo
arquivo = st.file_uploader("Escolha o arquivo Excel (.xlsx)", type="xlsx")

if arquivo is not None:
    # Leitura da base
    df_base = pd.read_excel(arquivo)

    # Normaliza os nomes das colunas (remove espaços e coloca tudo em maiúsculo)
    df_base.columns = df_base.columns.str.strip().str.upper()

    # Mostra as colunas disponíveis para debug
    st.write("Colunas carregadas:", df_base.columns.tolist())

    # Campo de busca
    termo_busca = st.text_input("Digite o termo ou código que deseja buscar:")

    if termo_busca:
        termos = termo_busca.strip().upper().split()

        try:
            # Filtro robusto com verificação de colunas
            if "CÓDIGO" in df_base.columns and "DESCRIÇÃO" in df_base.columns:
                filtro = df_base.apply(
                    lambda row: any(termo in str(row["CÓDIGO"]).upper() or termo in str(row["DESCRIÇÃO"]).upper() for termo in termos),
                    axis=1
                )

                resultados = df_base[filtro]

                if not resultados.empty:
                    st.success(f"{len(resultados)} itens encontrados.")
                    st.dataframe(resultados)
                else:
                    st.warning("Nenhum resultado encontrado.")
            else:
                st.error("As colunas 'CÓDIGO' e 'DESCRIÇÃO' não foram encontradas no arquivo.")
        except Exception as e:
            st.error(f"Ocorreu um erro durante a busca: {e}")
else:
    st.info("Envie um arquivo Excel para iniciar.")
