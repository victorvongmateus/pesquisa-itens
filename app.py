import streamlit as st
import pandas as pd

# Título
st.set_page_config(page_title="Pesquisa de Itens", layout="wide")
st.title("🔍 Pesquisa de Itens - Bioenergética Aroeira")
st.image("logo_aroeira.png", width=200)

# Upload da planilha
arquivo = "Pesquisa de itens.xlsm"
try:
    df = pd.read_excel(arquivo, sheet_name="Base")
except Exception as e:
    st.error(f"Erro ao ler o arquivo: {e}")
    st.stop()

# Entrada do usuário
codigos = st.text_area("Digite os códigos separados por vírgula ou enter:")

if st.button("Buscar"):
    if codigos.strip() == "":
        st.warning("Digite ao menos um código para buscar.")
    else:
        # Processa os códigos
        lista_codigos = [c.strip() for c in codigos.replace(",", "\n").splitlines() if c.strip()]

        # Filtra o DataFrame
        resultado = df[df["Código"].astype(str).isin(lista_codigos)]

        if resultado.empty:
            st.warning("Nenhum resultado encontrado.")
        else:
            # Mostra a tabela com colunas específicas
            colunas_desejadas = [
                "Código", "Descrição", "Descrição reduzida", "Situação",
                "Unidade", "Mín", "Máx", "R$ médio"
            ]
            resultado = resultado[colunas_desejadas]
            st.success(f"{len(resultado)} item(ns) encontrado(s):")
            st.dataframe(resultado)

            # Botão para baixar resultado
            csv = resultado.to_csv(index=False).encode("utf-8")
            st.download_button("📥 Baixar resultados em CSV", csv, "resultado.csv", "text/csv")
