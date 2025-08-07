import streamlit as st
import pandas as pd

# Título
st.title("🔍 Pesquisa de Itens - Bioenergética Aroeira")

# Entrada do usuário
entrada = st.text_area("Digite os códigos ou palavras separadas por vírgula ou enter:")

if st.button("Buscar"):
    try:
        # Leitura da aba 'Base'
        df = pd.read_excel("Pesquisa de itens.xlsm", sheet_name="Base")

        # Normaliza os nomes das colunas
        df.columns = [col.strip().lower() for col in df.columns]

        # Trata a entrada
        termos = [t.strip().lower() for t in entrada.replace("\n", ",").split(",") if t.strip()]

        # Concatena os textos das colunas por linha
        df["busca"] = df.astype(str).apply(lambda row: " ".join(row.values).lower(), axis=1)

        # Filtra linhas com qualquer termo
        resultado = df[df["busca"].apply(lambda texto: any(t in texto for t in termos))]

        # Remove a coluna auxiliar e o índice
        resultado = resultado.drop(columns=["busca"]).reset_index(drop=True)

        # Exibir resultado
        st.success(f"{len(resultado)} item(ns) encontrado(s).")
        st.dataframe(resultado, use_container_width=True)

    except Exception as e:
        st.error(f"Ocorreu um erro: {e}")
