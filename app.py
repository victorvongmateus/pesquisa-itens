import streamlit as st
import pandas as pd
from PIL import Image

# Configurações da página
st.set_page_config(layout="wide")

# Carrega logo
logo = Image.open("logo_aroeira.png")

# Layout com logo à esquerda e título ao lado
col1, col2 = st.columns([1, 5])
with col1:
    st.image(logo, width=150)
with col2:
    st.markdown("<h1 style='margin-bottom: 5px;'>Pesquisa de Itens – Bioenergética Aroeira</h1>", unsafe_allow_html=True)
    st.markdown("<h5 style='color: gray; font-weight: bold;'>Desenvolvido por Victor von Glehn – Especialista de Engenharia Agrícola</h5>", unsafe_allow_html=True)

# Campo de busca
termo_busca = st.text_input("Digite o termo ou código que deseja buscar:")

# Leitura da base
df_base = pd.read_excel("Pesquisa de itens.xlsm", sheet_name="Base", engine="openpyxl")

# Preenchendo valores nulos
df_base.fillna("", inplace=True)

# Filtrando colunas relevantes
colunas_desejadas = ["CODIGO", "DESCRICAO", "DESCRIÇÃO ANTIGA", "SITUACAO", "MIN", "MAX", "R$ MÉDIO"]
df_base = df_base[colunas_desejadas]

# Aplicando filtro exato (todos os termos precisam estar presentes)
if termo_busca:
    termos = termo_busca.lower().split()
    filtro = df_base.apply(lambda row: all(
        all(t in str(row[col]).lower() for t in termos)
        for col in ["DESCRICAO", "DESCRIÇÃO ANTIGA", "CODIGO"]
    ), axis=1)
    resultados = df_base[filtro]
else:
    resultados = pd.DataFrame(columns=df_base.columns)

# Formatando coluna de preço
if not resultados.empty:
    resultados["R$ MÉDIO"] = resultados["R$ MÉDIO"].apply(
        lambda x: f"R$ {x:.2f}" if isinstance(x, (int, float)) and x != 0 else "-"
    )
    resultados["MIN"] = resultados["MIN"].apply(lambda x: "-" if x == 0 else x)
    resultados["MAX"] = resultados["MAX"].apply(lambda x: "-" if x == 0 else x)

# Resultados
if termo_busca:
    if not resultados.empty:
        st.success(f"{len(resultados)} item(ns) encontrado(s).")
        st.dataframe(resultados.reset_index(drop=True), use_container_width=True, hide_index=True)
    else:
        st.warning("Nenhum resultado encontrado.")
