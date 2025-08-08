import streamlit as st
import pandas as pd

# Título e logo
st.set_page_config(page_title="Pesquisa de Itens - Bioenergética Aroeira", layout="wide")
col1, col2 = st.columns([1, 9])
with col1:
    st.image("logo_aroeira.png", width=100)
with col2:
    st.markdown("<h1 style='margin-bottom: 0;'>🔍 Pesquisa de Itens - Bioenergética Aroeira</h1>", unsafe_allow_html=True)
    st.caption("Desenvolvido por Victor von Glehn - Especialista de Engenharia Agrícola")

# Caixa de texto para entrada
st.markdown("Digite os códigos ou palavras separadas por vírgula ou enter:")
entrada = st.text_area("", height=50)

# Botão de busca
if st.button("Buscar"):
    try:
        # Leitura e padronização da planilha
        df = pd.read_excel("Pesquisa de itens.xlsm", sheet_name="Base")
        df.columns = df.columns.str.lower().str.strip()
        df = df.astype(str).apply(lambda col: col.str.lower())

        # Separar termos digitados
        termos = [t.strip().lower() for t in entrada.replace("\n", ",").split(",") if t.strip()]

        if not termos:
            st.warning("Digite pelo menos um termo para buscar.")
        else:
            # Filtro: verifica se algum termo aparece nas colunas 'codigo' ou 'descricao'
            resultado = df[
                df['codigo'].str.contains('|'.join(termos), na=False) |
                df['descricao'].str.contains('|'.join(termos), na=False)
            ]

            if resultado.empty:
                st.warning("Nenhum item encontrado.")
            else:
                st.success(f"{len(resultado)} item(ns) encontrado(s).")
                st.dataframe(resultado.dropna(axis=1, how='all'), use_container_width=True)

    except FileNotFoundError:
        st.error("Erro ao carregar planilha: Arquivo 'Pesquisa de itens.xlsm' não encontrado.")
    except Exception as e:
        st.error(f"Erro ao carregar planilha: {e}")
