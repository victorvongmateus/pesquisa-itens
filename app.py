import streamlit as st
import pandas as pd

st.set_page_config(page_title="Pesquisa de Itens - Bioenergética Aroeira", layout="centered")

# Logo
st.image("logo_aroeira.png", width=100)

# Título
st.markdown("## 🔍 Pesquisa de Itens - Bioenergética Aroeira")

# Upload da planilha
uploaded_file = "Pesquisa de itens.xlsm"

@st.cache_data
def carregar_dados():
    try:
        df = pd.read_excel(uploaded_file, sheet_name="Base")
        return df
    except Exception as e:
        st.error(f"Erro ao carregar a planilha: {e}")
        return pd.DataFrame()

df = carregar_dados()

# Entrada do usuário
codigos = st.text_area("Digite os códigos separados por vírgula ou enter:", height=100)

# Botão de busca
if st.button("Buscar") and codigos:
    # Processamento dos códigos
    lista_codigos = [
        c.strip()
        for c in codigos.replace(",", "\n").splitlines()
        if c.strip()
    ]

    if df.empty:
        st.warning("Nenhum dado foi carregado.")
    else:
        # Tenta localizar a coluna com nome semelhante a "Código"
        col_codigo = next((col for col in df.columns if "código" in col.lower()), None)

        if not col_codigo:
            st.error("Coluna 'Código' não encontrada na planilha.")
        else:
            resultado = df[df[col_codigo].astype(str).isin(lista_codigos)]

            if resultado.empty:
                st.warning("Nenhum item encontrado.")
            else:
                st.success(f"{len(resultado)} item(ns) encontrado(s).")
                st.dataframe(resultado)
