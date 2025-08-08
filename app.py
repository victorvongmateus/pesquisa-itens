import streamlit as st
import pandas as pd
from PIL import Image

# Configurações da página
st.set_page_config(page_title="Pesquisa de Itens", layout="wide")

# Carrega o logo
logo = Image.open("logo_aroeira.png")

# Layout superior: logo à esquerda, título e autor à direita
col1, col2 = st.columns([1, 6])
with col1:
    st.image(logo, width=120)
with col2:
    st.markdown(
        """
        <h1 style='text-align: left; margin-bottom: 0;'>Pesquisa de Itens – Bioenergética Aroeira</h1>
        <p style='text-align: left; font-weight: bold;'>Desenvolvido por Victor von Glehn Mateus</p>
        """,
        unsafe_allow_html=True
    )

# Campo de busca
st.markdown("###")
termo_busca = st.text_input("Digite o termo ou código que deseja buscar:")

# Carrega a planilha
@st.cache_data
def carregar_dados():
    df = pd.read_excel("Pesquisa de itens.xlsm", sheet_name="Base")
    return df

df_base = carregar_dados()

# Filtragem com busca específica
if termo_busca:
    termo_busca = termo_busca.strip().upper()
    filtro = df_base.apply(
        lambda row: termo_busca in str(row.get("DESCRICAO", "")).upper()
                 or termo_busca in str(row.get("DESCRIÇÃO ANTIGA", "")).upper()
                 or termo_busca in str(row.get("CODIGO", "")).upper(),
