import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Pesquisa de Itens - Bioenergética Aroeira", layout="wide")

# Cabeçalho com logo e título
col1, col2 = st.columns([1, 10])
with col1:
    st.image("logo_aroeira.png", width=120)
with col2:
    st.markdown("<p style='text-align: center; font-size: 14px;'>Desenvolvido por Victor von Glehn - Especialista de Engenharia Agrícola</p>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center;'>Pesquisa de Itens - Bioenergética Aroeira</h1>", unsafe_allow_html=True)

# Entrada de busca
st.write("Digite os códigos ou palavras separadas por vírgula ou enter:")
entrada = st.text_area("", height=40)

# Botão de busca
if st.button("Buscar"):
    try:
        # Carregar planilha
        df = pd.read_excel("Pesquisa de itens.xlsm", sheet_name="Base")

        # Converter para string e caixa baixa
        df = df.astype(str).apply(lambda col: col.str.lower())

        # Processar entrada
        termos = [termo.strip().lower() for termo in entrada.replace('\n', ',').split(',') if termo.strip()]

        # Filtrar resultados
        resultado = df[df.apply(lambda row: any(termo in row['codigo'] or termo in row['descricao'] for termo in termos), axis=1)]

        if not resultado.empty:
            st.success(f"{len(resultado)} item(ns) encontrado(s).")
            st.dataframe(resultado.reset_index(drop=True))
        else:
            st.warning("Nenhum item encontrado.")

    except Exception as e:
        st.error(f"Erro ao carregar planilha: {e}")
