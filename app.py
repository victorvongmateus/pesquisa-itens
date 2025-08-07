
import streamlit as st
import pandas as pd

# Logo e título
col1, col2 = st.columns([1, 5])
with col1:
    st.image("logo_aroeira.png", width=80)
with col2:
    st.markdown("## PESQUISA DE ITENS")
    st.markdown("Desenvolvido por Victor von Glehn – Especialista de Engenharia Agrícola")

# Carregar base de dados
@st.cache_data
def carregar_dados():
    return pd.read_excel("Pesquisa de itens.xlsm", sheet_name="Base")

df = carregar_dados()

# Abas
aba = st.tabs(["Consulta por termo", "Verificação por lotes"])

with aba[0]:
    termo = st.text_input("Termo")
    if termo:
        termos = termo.lower().split()
        resultado = df[df.apply(lambda row: all(t in str(row["Código"]).lower() + str(row["Descrição"]).lower() for t in termos), axis=1)]
        st.dataframe(resultado)

with aba[1]:
    codigos = st.text_area("Cole os códigos (um por linha ou separados por vírgula)")
    if codigos:
       lista_codigos = [c.strip() for c in codigos.replace(",", "\n").split()]
").splitlines() if c.strip()]
        resultado = df[df["Código"].astype(str).isin(lista_codigos)]
        st.dataframe(resultado)
