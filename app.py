import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Pesquisa de Itens - Bioenergética Aroeira", layout="wide")

# Título superior
st.markdown(
    "<p style='text-align: center; font-size:14px'>Desenvolvido por Victor von Glehn - Especialista de Engenharia Agrícola</p>",
    unsafe_allow_html=True
)

# Logo da Aroeira
st.image("logo_aroeira.png", width=100)

# Título principal
st.markdown("<h1 style='text-align: center;'>Pesquisa de Itens - Bioenergética Aroeira</h1>", unsafe_allow_html=True)

# Campo de entrada
st.write("Digite os códigos ou palavras separadas por vírgula ou enter:")
entrada = st.text_area("", height=50)

# Botão de busca
if st.button("Buscar"):

    try:
        # Carregando a planilha
        df = pd.read_excel("Pesquisa de itens.xlsm")

        # Padroniza nomes de colunas
        df.columns = df.columns.str.strip().str.lower()

        # Verifica colunas obrigatórias
        colunas_obrigatorias = ['codigo', 'descricao']
        for col in colunas_obrigatorias:
            if col not in df.columns:
                st.error(f"Coluna '{col}' não encontrada na planilha.")
                st.stop()

        # Quebra a entrada em termos
        termos = [t.strip().lower() for t in entrada.replace(",", "\n").splitlines() if t.strip()]

        # Filtra por qualquer termo na coluna código ou descrição
        resultado = df[df.apply(lambda row: any(
            termo in str(row['codigo']).lower() or termo in str(row['descricao']).lower()
            for termo in termos), axis=1)]

        if not resultado.empty:
            st.success(f"{len(resultado)} item(ns) encontrado(s).")

            # Exibe o resultado sem índice (sem a primeira coluna numérica)
            st.dataframe(
                resultado.reset_index(drop=True).rename(columns=str.upper),
                use_container_width=True
            )
        else:
            st.warning("Nenhum item encontrado.")

    except Exception as e:
        st.error(f"Erro ao carregar planilha: {e}")
