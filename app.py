import streamlit as st
import pandas as pd

# Título
st.title("🔎 Pesquisa de Itens - Bioenergética Aroeira")

# Carrega os dados da aba 'Base'
@st.cache_data
def carregar_dados():
    try:
        df = pd.read_excel("Pesquisa de itens.xlsm", sheet_name="Base")
        df.columns = df.columns.str.strip()  # Remove espaços em branco das colunas
        return df
    except Exception as e:
        st.error(f"Erro ao carregar a planilha: {e}")
        return pd.DataFrame()

df = carregar_dados()

# Entrada do usuário
entrada = st.text_area("Digite os códigos ou palavras separadas por vírgula ou enter:")

# Botão de busca
if st.button("Buscar"):
    if df.empty:
        st.warning("A planilha não foi carregada corretamente.")
    elif entrada.strip() == "":
        st.warning("Digite algo para pesquisar.")
    else:
        termos = [termo.strip().lower() for termo in entrada.replace("\n", ",").split(",") if termo.strip()]

        # Cria uma coluna para busca combinada
        df["busca"] = (
            df.astype(str)
            .apply(lambda row: " ".join(row.values).lower(), axis=1)
        )

        # Filtra resultados
        resultado = df[df["busca"].apply(lambda texto: all(t in texto for t in termos))]

        if resultado.empty:
            st.error("Nenhum item encontrado.")
        else:
            st.success(f"{len(resultado)} item(ns) encontrado(s).")
            st.dataframe(resultado.drop(columns=["busca"]))
