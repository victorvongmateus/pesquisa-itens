import streamlit as st
import pandas as pd

st.set_page_config(page_title="Pesquisa de Itens - Bioenergética Aroeira", layout="centered")

st.image("logo_aroeira.png", width=100)
st.markdown("## 🔍 Pesquisa de Itens - Bioenergética Aroeira")

uploaded_file = "Pesquisa de itens.xlsm"

@st.cache_data
def carregar_dados():
    try:
        df = pd.read_excel(uploaded_file, sheet_name="Base")
        return df
    except Exception as e:
        st.error(f"Erro ao carregar a planilha: {e}")
        return pd.DataFrame()

df = carregar_dados()

entrada = st.text_area("Digite os códigos ou palavras separadas por vírgula ou enter:", height=100)

if st.button("Buscar") and entrada:
    termos = [t.strip().lower() for t in entrada.replace(",", "\n").splitlines() if t.strip()]

    if df.empty:
        st.warning("Nenhum dado carregado.")
    else:
        # Procurar colunas relevantes
        colunas_validas = df.columns.str.lower()
        col_codigo = next((c for c in df.columns if "código" in c.lower()), None)
        col_descricao = next((c for c in df.columns if "descrição" in c.lower()), None)

        if not col_codigo and not col_descricao:
            st.error("Colunas de código ou descrição não encontradas.")
        else:
            df_str = df.astype(str).apply(lambda x: x.str.lower())

            # Filtro por termos
            resultado = df[
                df_str.apply(
                    lambda row: any(
                        termo in row.get(col_codigo, "") or termo in row.get(col_descricao, "")
                        for termo in termos
                    ),
                    axis=1,
                )
            ]

            if resultado.empty:
                st.warning("Nenhum item encontrado.")
            else:
                st.success(f"{len(resultado)} item(ns) encontrado(s).")
                st.dataframe(resultado)

