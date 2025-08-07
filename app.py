import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

st.image("logo_aroeira.png", width=80)
st.markdown("## 🔍 Pesquisa de Itens - Bioenergética Aroeira")

uploaded_file = "Pesquisa de itens.xlsm"

try:
    df = pd.read_excel(uploaded_file, sheet_name="Base")
except Exception as e:
    st.error(f"Erro ao carregar planilha: {e}")
    st.stop()

termo = st.text_area("Digite os códigos ou palavras separadas por vírgula ou enter:")

if st.button("Buscar"):
    if not termo.strip():
        st.warning("Digite ao menos um código ou palavra.")
    else:
        codigos = termo.replace(",", "\n").splitlines()
        lista_codigos = [c.strip() for c in codigos if c.strip()]

        filtro = pd.Series([False] * len(df))
        for c in lista_codigos:
            filtro |= df.apply(lambda row: row.astype(str).str.contains(c, case=False, na=False).any(), axis=1)

        resultado = df[filtro]

        total = len(resultado)
        st.success(f"{total} item(ns) encontrado(s).")
        st.dataframe(resultado, use_container_width=True)
