import streamlit as st
import pandas as pd

st.set_page_config(page_title="Pesquisa de Itens", layout="centered")
st.title("Pesquisa de Itens")

# Upload do arquivo Excel
arquivo = st.file_uploader("Escolha o arquivo Excel (.xlsx)", type=["xlsx", "xls"])

if arquivo is not None:
    try:
        # Tenta carregar a primeira aba automaticamente
        df_base = pd.read_excel(arquivo)

        # Normaliza os nomes das colunas (remove espaços e coloca tudo em maiúsculas)
        df_base.columns = df_base.columns.str.strip().str.upper()

        # Mostra as colunas carregadas
        st.write("✅ Colunas carregadas:", df_base.columns.tolist())

        # Verifica se as colunas obrigatórias existem
        if "CÓDIGO" in df_base.columns and "DESCRIÇÃO" in df_base.columns:
            # Campo de busca
            termo_busca = st.text_input("Digite o termo ou código que deseja buscar:")

            if termo_busca:
                termos = termo_busca.strip().upper().split()

                # Aplica o filtro na base
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
                    st.warning("Nenhum resultado encontrado para o(s) termo(s) informado(s).")
        else:
            st.error("❌ As colunas 'CÓDIGO' e 'DESCRIÇÃO' não foram encontradas no arquivo.")
            st.stop()

    except Exception as e:
        st.error(f"Erro ao processar o arquivo: {e}")
else:
    st.info("📥 Envie um arquivo Excel para iniciar.")
