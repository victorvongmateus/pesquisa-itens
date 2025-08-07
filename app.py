import streamlit as st
import pandas as pd

# --- Configurações iniciais da página ---
st.set_page_config(
    page_title="Pesquisa de Itens - Bioenergética Aroeira",
    layout="wide",
)

# --- Logo e título ---
col1, col2 = st.columns([1, 20])
with col1:
    st.image("logo_aroeira.png", width=80)
with col2:
    st.markdown(
        "<h1 style='color:#001858; font-weight:700;'>🔍 Pesquisa de Itens - Bioenergética Aroeira</h1>",
        unsafe_allow_html=True
    )

# --- Caixa de entrada ---
st.markdown("Digite os códigos ou palavras separadas por vírgula ou enter:")
codigos = st.text_area("", height=70)

# --- Botão de busca ---
if st.button("Buscar"):
    try:
        # --- Leitura da aba "Base" ---
        df = pd.read_excel("Pesquisa de itens.xlsm", sheet_name="Base")

        # --- Limpeza e tratamento dos termos de busca ---
        lista_codigos = [c.strip().lower() for c in codigos.replace(",", "\n").splitlines() if c.strip()]

        # --- Padroniza colunas ---
        df["Código"] = df["Código"].astype(str)
        df["Descrição"] = df["Descrição"].astype(str)
        df["Descrição reduzida"] = df.get("Descrição reduzida", "").astype(str)

        # --- Concatena os campos de busca ---
        df["busca"] = df["Código"].str.lower() + " " + df["Descrição"].str.lower() + " " + df["Descrição reduzida"].str.lower()

        # --- Filtro de resultados ---
        resultado = df[df["busca"].apply(
            lambda texto: any(term in texto for term in lista_codigos)
        )]

        # --- Mostra resultados ---
        st.success(f"{len(resultado)} item(ns) encontrado(s).")
        st.dataframe(resultado.drop(columns=["busca"]).reset_index(drop=True), use_container_width=True)

    except Exception as e:
        st.error(f"Ocorreu um erro: {e}")
