import streamlit as st
import pandas as pd

# Título
st.title("🔍 Pesquisa de Itens - Bioenergética Aroeira")

# Campo de entrada
entrada = st.text_area("Digite os códigos ou palavras separadas por vírgula ou enter:")

# Botão de busca
if st.button("Buscar"):
    try:
        # Carrega a planilha e define aba correta
        df = pd.read_excel("Pesquisa de itens.xlsm", sheet_name="Base")

        # Padroniza nomes das colunas (tudo minúsculo e sem espaços)
        df.columns = [col.strip().lower() for col in df.columns]

        # Cria uma coluna auxiliar com todas as informações unidas
        df["busca"] = df.astype(str).apply(lambda row: " ".join(row.values).lower(), axis=1)

        # Prepara termos de busca
        termos = [t.strip().lower() for t in entrada.replace("\n", ",").split(",") if t.strip()]

        # Aplica filtro
        resultado = df[df["busca"].apply(lambda texto: any(t in texto for t in termos))]

        # Remove a coluna auxiliar e reseta o índice
        resultado = resultado.drop(columns=["busca"]).reset_index(drop=True)

        # Exibe os resultados sem a coluna de índice
        st.success(f"{len(resultado)} item(ns) encontrado(s).")
        st.dataframe(resultado, use_container_width=True)

    except Exception as e:
        st.error(f"Ocorreu um erro: {e}")
