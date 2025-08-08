import streamlit as st
import pandas as pd
from PIL import Image

st.set_page_config(page_title="Pesquisa de Itens", layout="centered")

# Logo centralizada
try:
    logo = Image.open("logo_aroeira.png")
    st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    st.image(logo, width=200)
    st.markdown("</div>", unsafe_allow_html=True)
except:
    pass

# Desenvolvido por (negrito, centralizado)
st.markdown(
    """
    <div style="text-align: center; font-size: 16px; font-weight: bold; margin-top: -10px; margin-bottom: 30px;">
        Desenvolvido por Victor von Glehn Mateus
    </div>
    """,
    unsafe_allow_html=True
)

# Título atualizado
st.markdown("<h1 style='text-align: center;'>Pesquisa de Itens – Bioenergética Aroeira</h1>", unsafe_allow_html=True)

# Carrega a base
df_base = pd.read_excel("Pesquisa de itens.xlsm", engine="openpyxl")
df_base.columns = df_base.columns.str.strip().str.upper()

# Campo de busca
termo_busca = st.text_input("Digite o ter
