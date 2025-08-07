import streamlit as st
import pandas as pd

# --- Configuração da página
st.set_page_config(page_title="Pesquisa de Itens", layout="wide")

# --- Frase superior
st.markdown("<p style='text-align: center; font-size:14px;'>Desenvolvido por Victor von Glehn - Especialista de Engenharia Agrícola</p>", unsafe_allow_html=True)

# --- Logo + Título
col1, col2 = st.columns([1, 6])

with col1:
    st.image("logo_aroeira.png", width=100)

with col2:
    st.markdown("<h1 style='padding-top: 25px;'>Pesquisa de Itens - Bioenergética Aroeira</h1>", unsafe_allow_html=True)

# --- Instruções
st.write("Digite os códigos ou palavras separadas por vírgula ou enter:")

# --- Campo de busca
entrada = st.text_area(" ", height=40)
botao = st.button("Buscar")

# --- Carrega a planilha
try:
    df = pd.read_excel("Pesquisa de itens.xlsx", sheet_name=None)
except Exception as e:
    st.error(f"Erro ao carregar planilha: {e}")
    st.stop()

# --- Concatena os dados das abas
dados = pd.concat(df.values(), ignore_index=True)

# --- Limpa os nomes das colunas
dados.columns = [col.lower().strip() for col in dados.columns]

# --- Busca
if botao and entrada.strip():
    termos = [termo.strip().lower() for termo in entrada.replace(",", "\n").splitlines() if termo.strip()]
    
    def contem_termo(row):
        texto = ' '.join([str(v).lower() for v in row.values])
        return any(t in texto for t in termos)

    try:
        encontrados = dados[dados.apply(contem_termo, axis=1)]
        if not encontrados.empty:
            st.success(f"{len(encontrados)} item(ns) encontrado(s).")
            st.dataframe(encontrados.reset_index(drop=True), use_container_width=True)
        else:
            st.warning("Nenhum item encontrado com os termos fornecidos.")
    except Exception as e:
        st.error(f"Ocorreu um erro: {e}")
