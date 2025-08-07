import streamlit as st
import pandas as pd

# --- Configurações da página ---
st.set_page_config(
    page_title="Pesquisa de Itens - Bioenergética Aroeira",
    layout="wide"
)

# --- Logo e título ---
col1, col2 = st.columns([1, 10])
with col1:
    st.image("arvore.png", width=80)
with col2:
    st.markdown("<h1 style='color:#002060;'>🔍 Pesquisa de Itens - Bioenergética Aroeira</h1>", unsafe_allow_html=True)

st.markdown("Digite os códigos ou palavras separadas por vírgula ou enter:")

# --- Campo de entrada do usuário ---
codigos = st.text_area(" ", placeholder="Ex: corrente randon, rolete inferior", height=70)
botao = st.button("Buscar")

# --- Ação de busca ---
if botao and codigos.strip():
    try:
        # Leitura da planilha na aba "Base"
        df = pd.read_excel("Pesquisa de itens.xlsm", sheet_name="Base")
        df.columns = df.columns.str.strip()  # remove espaços extras

        # Verifica se a coluna "Código" existe
        if not any(col.lower() == "código" for col in df.columns.str.lower()):
            st.error(f"Coluna 'Código' não encontrada. Colunas disponíveis: {list(df.columns)}")
            st.stop()

        # Padroniza os nomes das colunas
        df.columns = df.columns.str.strip().str.lower()
        df.rename(columns={
            "código": "codigo",
            "descrição": "descricao",
            "descrição reduzida": "descricao_reduzida"
        }, inplace=True)

        # Trata os termos digitados
        lista_codigos = [c.strip().lower() for c in codigos.replace(",", "\n").splitlines() if c.strip()]

        # Concatena colunas relevantes para a busca
        df["codigo"] = df["codigo"].astype(str)
        df["descricao"] = df["descricao"].astype(str)
        df["descricao_reduzida"] = df.get("descricao_reduzida", "").astype(str)

        df["busca"] = df["codigo"] + " " + df["descricao"] + " " + df["descricao_reduzida"]

        # Filtra os resultados com base na lista de códigos/termos
        resultado = df[df["busca"].apply(lambda texto: any(term in texto for term in lista_codigos))]

        # Mostra resultado
        st.success(f"{len(resultado)} item(ns) encontrado(s).")
        st.dataframe(resultado.drop(columns=["busca"]).reset_index(drop=True), use_container_width=True)

    except Exception as e:
        st.error(f"Ocorreu um erro: {e}")
