import streamlit as st
import pandas as pd
from PIL import Image

st.set_page_config(page_title="Pesquisa de Itens – Bioenergética Aroeira", layout="wide")

# Carregar logo
logo = Image.open("logo_aroeira.png")

# Cabeçalho com logo à esquerda e título à direita
col1, col2 = st.columns([1, 6])
with col1:
    st.image(logo, width=150)
with col2:
    st.markdown("<h1 style='margin-bottom: 5px;'>Pesquisa de Itens – Bioenergética Aroeira</h1>", unsafe_allow_html=True)
    st.markdown("<b>Desenvolvido por Victor von Glehn – Especialista de Engenharia Agrícola</b>", unsafe_allow_html=True)

st.markdown("---")

# Campo de busca
termo_busca = st.text_input("Digite o termo ou código que deseja buscar:")

# Carregar dados
@st.cache_data
def carregar_dados():
    df = pd.read_excel("Pesquisa de itens.xlsm", sheet_name="Base", engine="openpyxl")
    df.columns = df.columns.str.strip().str.upper()
    return df

df_base = carregar_dados()

# Define colunas desejadas (em maiúsculas)
colunas_desejadas = ["CODIGO", "DESCRICAO", "DESCRIÇÃO ANTIGA", "SITUACAO", "MIN", "MAX", "R$ MÉDIO"]
colunas_existentes = [col for col in colunas_desejadas if col in df_base.columns]

# Seleciona só colunas existentes
df_base = df_base[colunas_existentes]

# Busca específica
if termo_busca:
    termo = termo_busca.strip().lower()
    filtro = df_base.apply(
        lambda row: termo in str(row.get("DESCRICAO", "")).lower()
                 or termo in str(row.get("DESCRIÇÃO ANTIGA", "")).lower()
                 or termo in str(row.get("CODIGO", "")).lower(),
        axis=1
    )
    df_filtrado = df_base[filtro]
else:
    df_filtrado = pd.DataFrame(columns=df_base.columns)

# Formata R$ MÉDIO
if "R$ MÉDIO" in df_filtrado.columns and not df_filtrado.empty:
    df_filtrado["R$ MÉDIO"] = df_filtrado["R$ MÉDIO"].apply(
        lambda x: f"R$ {x:,.2f}" if pd.notnull(x) and isinstance(x, (int, float)) else "-"
    )

# Resultados
if termo_busca:
    if not df_filtrado.empty:
        st.success(f"{len(df_filtrado)} item(ns) encontrado(s).")
        st.dataframe(df_filtrado.reset_index(drop=True), use_container_width=True, hide_index=True)
    else:
        st.warning("Nenhum resultado encontrado.")
