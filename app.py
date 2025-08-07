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

        # --- Verifica se a coluna 'Código' existe ---
        if "Código" not in df.columns and "Código".lower() not in df.columns.str.lower():
            st.error("Coluna 'Código' não encontrada na planilha.")
        else:
            # --- Padroniza colunas para busca textual também nas descrições ---
            df["Código"] = df["Código"].astype(str)
            df["Descrição"] = df["Descrição"].astype(str)
            df["Descrição reduzida"] = df.get("Descrição reduzida", "").astype(str)

            # --- Concatena os campo
