import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Pesquisa de Itens - Bioenergética Aroeira", layout="wide")

# Esconder header, menu e rodapé do Streamlit
st.markdown("""
    <style>
        #MainMenu, footer, header {visibility: hidden;}
        .block-container {
            padding-top: 2rem;
        }
    </style>
""", unsafe_allow_html=True)

# Frase de autoria no topo
st.markdown(
    "<p style='text-align: center; font-size:14px;'>Desenvolvido por Victor von Glehn - Especialista de Engenharia Agrícola</p>",
    unsafe_allow_html=True
)

# Logo da Aroeira + Título
st.markdown("""
    <div style="display: flex; align-items: center; gap: 20px;">
        <img src="logo_aroeira.png" width="100"/>
        <h1>Pesquisa de Itens - Bioenergética Aroeira</h1>
    </div>
""", unsafe_allow_html=True)

# Campo de entrada
st.write("Digite os códigos ou palavras separadas por vírgula ou enter:")
entrada = st.text_area(" ", height=40)
botao = st.button("Buscar")

# Carregamento da planilha
try:
    sheets = pd.read_excel("Pesquisa de itens.xlsx", sheet_name=None)
    df = pd.concat(sheets.values(), ignore_index=True)
except Exception as e:
    st.error(f"Erro ao carregar planilha: {e}")
    st.stop()

# Padroniza os nomes das colunas
df.columns = [col.lower().strip() for col in df.columns]

# Ação de busca
if botao and entrada.strip():
    termos = [termo.strip().lower() for termo in entrada.replace(",", "\n").splitlines() if termo.strip()]

    def contem_termo(row):
        texto = " ".join([str(x).lower() for x in row.values])
        return any(t in texto for t in termos)

    resultado = df[df.apply(contem_termo, axis=1)]

    if not resultado.empty:
        st.success(f"{len(resultado)} item(ns) encontrado(s).")
        st.dataframe(resultado.reset_index(drop=True), use_container_width=True)
    else:
        st.warning("Nenhum item encontrado.")
