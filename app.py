import streamlit as st
import pandas as pd

# Créditos superiores
st.markdown("""
    <div style="text-align: center; font-size: 14px; color: gray;">
        Desenvolvido por Victor von Glehn - Especialista de Engenharia Agrícola
    </div>
""", unsafe_allow_html=True)

# Título com logo da empresa (substituindo a lupa)
st.markdown("""
    <div style="display: flex; align-items: center; gap: 20px;">
        <img src="https://raw.githubusercontent.com/victorvonmateus/NOME_DO_SEU_REPO/main/logo_aroeira.png" width="100"/>
        <h1>Pesquisa de Itens - Bioenergética Aroeira</h1>
    </div>
""", unsafe_allow_html=True)

st.write("Digite os códigos ou palavras separadas por vírgula ou enter:")

entrada = st.text_area("", height=50)

if st.button("Buscar"):
    try:
        df = pd.read_excel("Pesquisa de itens.xlsx")

        # Normaliza colunas
        df.columns = [col.strip().lower() for col in df.columns]

        termos = [termo.strip().lower() for termo in entrada.replace("\n", ",").split(",") if termo.strip()]

        resultado = df[df.apply(
            lambda row: any(
                termo in str(row[col]).lower()
                for termo in termos
                for col in ['codigo', 'descricao']
            ),
            axis=1
        )]

        if not resultado.empty:
            st.success(f"{len(resultado)} item(ns) encontrado(s).")
            st.dataframe(resultado.reset_index(drop=True))
        else:
            st.warning("Nenhum item encontrado.")

    except FileNotFoundError:
        st.error("Erro ao carregar planilha: Arquivo 'Pesquisa de itens.xlsx' não encontrado.")
    except Exception as e:
        st.error(f"Erro ao executar a pesquisa: {e}")
