import streamlit as st
import pandas as pd

# Título e assinatura
st.markdown(
    "<p style='text-align: center; color: gray;'>Desenvolvido por Victor von Glehn - Especialista de Engenharia Agrícola</p>",
    unsafe_allow_html=True
)
st.markdown("<h1 style='text-align: center;'>🔎 Pesquisa de Itens - Bioenergética Aroeira</h1>", unsafe_allow_html=True)

# Campo de busca
termo_busca = st.text_area("Digite os códigos ou palavras separadas por vírgula ou enter:")

# Botão de buscar
if st.button("Buscar"):
    try:
        # Leitura da planilha
        df = pd.read_excel("Pesquisa de itens.xlsm", sheet_name="Base")

        # Limpa e prepara os termos de busca
        termos = [t.strip().lower() for t in termo_busca.replace('\n', ',').split(',') if t.strip() != ""]

        # Garante que todos os campos relevantes estão em texto minúsculo para comparação
        colunas_texto = df.select_dtypes(include=["object"]).columns
        df_lower = df.copy()
        for col in colunas_texto:
            df_lower[col] = df_lower[col].astype(str).str.lower()

        # Concatena todos os textos da linha em uma coluna auxiliar
        df_lower["__concat"] = df_lower[colunas_texto].agg(" ".join, axis=1)

        # Filtra por qualquer termo que esteja contido
        mask = df_lower["__concat"].apply(lambda linha: any(termo in linha for termo in termos))
        resultados = df[mask]

        # Mostra quantos resultados e a tabela limpa, sem índice
        st.success(f"{len(resultados)} item(ns) encontrado(s).")
        st.dataframe(resultados.to_dict('records'), use_container_width=True)

    except FileNotFoundError:
        st.error("Arquivo 'Pesquisa de itens.xlsm' não encontrado no diretório.")
    except ValueError as ve:
        st.error(f"Ocorreu um erro: {ve}")
    except Exception as e:
        st.error(f"Ocorreu um erro inesperado: {e}")
