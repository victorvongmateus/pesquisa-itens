import streamlit as st
import pandas as pd

# Título
st.title("🔍 Pesquisa de Itens - Bioenergética Aroeira")

# Entrada de texto
entrada = st.text_area("Digite os códigos ou palavras separadas por vírgula ou enter:")

# Botão de busca
if st.button("Buscar"):
    try:
        # Leitura da planilha (apenas aba "Base")
        df = pd.read_excel("Pesquisa de itens.xlsm", sheet_name="Base")

        # Verifica se coluna 'Código' existe
        if 'Código' not in df.columns:
            st.error("Coluna 'Código' não encontrada na planilha.")
        else:
            # Trata a entrada
            termos = [t.strip().lower() for t in entrada.replace("\n", ",").split(",") if t.strip()]

            # Concatena todas as colunas em uma string de busca
            df["busca"] = df.astype(str).apply(lambda row: " ".join(row.values).lower(), axis=1)

            # Filtra se qualquer termo aparecer na linha
            resultado = df[df["busca"].apply(lambda texto: any(t in texto for t in termos))]

            # Remove a coluna de busca e reset o índice
            resultado = resultado.drop(columns=["busca"]).reset_index(drop=True)

            # Resultado
            st.success(f"{len(resultado)} item(ns) encontrado(s).")
            st.dataframe(resultado, use_container_width=True)

    except Exception as e:
        st.error(f"Ocorreu um erro: {e}")
