import streamlit as st
import pandas as pd

# Título superior
st.markdown(
    "<div style='text-align: center;'>"
    "<p style='font-size: 14px;'>Desenvolvido por Victor von Glehn - Especialista de Engenharia Agrícola</p>"
    "</div>",
    unsafe_allow_html=True
)

# Exibir a logo da Aroeira
st.image("logo_aroeira.png", width=120)

# Título principal
st.markdown("<h1 style='text-align: center;'>Pesquisa de Itens - Bioenergética Aroeira</h1>", unsafe_allow_html=True)

# Entrada de busca
termo = st.text_area("Digite os códigos ou palavras separadas por vírgula ou enter:")

# Botão de busca
if st.button("Buscar"):
    try:
        # Carregar planilha
        df = pd.read_excel("Pesquisa de itens.xlsm", sheet_name="Base")

        # Normalizar termos
        termos = [t.strip().lower() for t in termo.replace("\n", ",").split(",") if t.strip()]
        
        # Buscar
        resultado = df[df.apply(lambda row: any(t in str(row["codigo"]).lower() or t in str(row["descricao"]).lower() for t in termos), axis=1)]

        if not resultado.empty:
            st.success(f"{len(resultado)} item(ns) encontrado(s).")
            st.dataframe(resultado.reset_index(drop=True))
        else:
            st.warning("Nenhum item encontrado.")
    except FileNotFoundError:
        st.error("Erro ao carregar planilha: Arquivo 'Pesquisa de itens.xlsm' não encontrado.")
