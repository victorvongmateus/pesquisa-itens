import streamlit as st
import pandas as pd

# Carregamento da planilha
@st.cache_data
def carregar_dados():
    try:
        df = pd.read_excel("Pesquisa de itens.xlsm", sheet_name=None)
        aba = list(df.values())[0]
        aba.columns = aba.columns.str.upper()
        return aba
    except Exception as e:
        st.error(f"Erro ao carregar planilha: {e}")
        return pd.DataFrame()

df_base = carregar_dados()

# Interface
st.markdown(
    """
    <div style="display: flex; align-items: center; justify-content: center;">
        <img src="https://raw.githubusercontent.com/victorvonglehn/pesquisa-itens/main/logo_aroeira.png" 
             style="height: 100px; margin-right: 20px;">
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div style="text-align: center; font-size: 18px; color: gray; margin-bottom: -20px;">
        Desenvolvido por Victor von Glehn - Especialista de Engenharia Agrícola
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    "<h2 style='text-align: center;'>🔍 Pesquisa de Itens - Bioenergética Aroeira</h2>",
    unsafe_allow_html=True
)

termos = st.text_area("Digite os códigos ou palavras separadas por vírgula ou enter:")

if st.button("Buscar") and df_base is not None:
    termos_busca = [t.strip().upper() for t in termos.replace("\n", ",").split(",") if t.strip()]
    if termos_busca:
        col_busca = ['CÓDIGO', 'DESCRIÇÃO']
        df_base[col_busca[0]] = df_base[col_busca[0]].astype(str)

        resultado = df_base[df_base.apply(
            lambda row: any(
                termo in str(row['CÓDIGO']).upper() or termo in str(row['DESCRIÇÃO']).upper()
                for termo in termos_busca
            ), axis=1)]

        if not resultado.empty:
            st.success(f"{len(resultado)} ITEM(NS) ENCONTRADO(S).")

            # Processamento do DataFrame para exibição
            resultado = resultado.drop(columns=resultado.columns[0])
            resultado.columns = resultado.columns.str.upper()

            if 'R$ MÉDIO' in resultado.columns:
                resultado['R$ MÉDIO'] = resultado['R$ MÉDIO'].apply(
                    lambda x: f"R$ {x:,.2f}".replace(".", ",") if pd.notnull(x) else "-"
                )
            for col in ['MÍN', 'MÁX']:
                if col in resultado.columns:
                    resultado[col] = resultado[col].apply(lambda x: "-" if pd.isna(x) else x)

            st.dataframe(resultado)
        else:
            st.warning("Nenhum item encontrado com os critérios de busca.")
