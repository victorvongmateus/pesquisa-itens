from pathlib import Path
import streamlit as st
import pandas as pd

# Caminho para o arquivo Excel
ARQUIVO = "Pesquisa de itens.xlsm"
ABA = "Base"

st.set_page_config(page_title="Pesquisa de Itens", layout="wide")

# Frase de autoria
st.markdown(
    "<p style='text-align:center; font-size:16px; color:gray;'>"
    "Desenvolvido por Victor von Glehn - Especialista de Engenharia Agrícola"
    "</p>",
    unsafe_allow_html=True
)

# Título da aplicação
st.markdown("<h1 style='text-align:center;'>🔍 Pesquisa de Itens - Bioenergética Aroeira</h1>", unsafe_allow_html=True)

# Campo de entrada
entrada = st.text_area("Digite os códigos ou palavras separadas por vírgula ou enter:", height=70)

# Botão de busca
if st.button("Buscar"):
    try:
        # Carrega a planilha
        df = pd.read_excel(ARQUIVO, sheet_name=ABA)

        # Garante que
