import streamlit as st
import pandas as pd
import base64

# Função para converter imagem em base64
def get_base64_logo():
    with open("logo_aroeira.png", "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Carregar a planilha e renomear as colunas para maiúsculas
@st.cache_data
def carregar_dados():
    df = pd.read_excel("Pesquisa de itens.xlsm", sheet_name=0)
    df.columns = [col.upper() for col in df.columns]
    for col in ["MÍN", "MÁX", "R$ MÉDIO"]:
        if col in df.columns:
            df[col] = df[col].apply(lambda x: "-" if pd.isna(x) or x == 0 else f"R$ {x:.2f}" if col == "R$ MÉDIO" else int(x))
    return df

# Exibir logo
logo_base64 = get_base64_logo()
st.markdown(
    f"<div style='text-align: center'><img src='data:image/png;base64,{logo_base64}' width='140'></div>",
    unsafe_allow_html=True,
)

# Título e subtítulo centralizados
st.markdown(
    "<h5 style='text-align: center; color: black;'>Desenvolvido por Victor von Glehn - Especialista de Engenharia Agrícola</h5>",
    unsafe_allow_html=True,
)
st.markdown(
    "<h2 style='text-align: center; color: black;'>Pesquisa de Itens - Bioenergética Aroeira</h2>",
    unsafe_allow_html=True,
)

# Campo de busca
st.write("Digite os códigos ou palavras separadas por vírgula ou enter:")
entrada = st.text_area("", height=60)

# Botão
if st.button("Buscar"):
    if entrada.strip() == "":
        st.warning("Digite ao menos um termo para buscar.")
    else:
        termos = [t.strip().upper() for t in entrada.replace(",", "\n").splitlines() if t.strip() != ""]

        df_base = carregar_dados()

        # Converter as colunas relevantes para string
        col_busca = ["CÓDIGO", "DESCRIÇÃO"]
        for col in col_busca:
            if col in df_base.columns:
                df_base[col] = df_base[col].astype(str).str.upper()

        # Buscar itens que contenham algum dos termos
        filtro = df_base.apply(
            lambda row: any(termo in row["CÓDIGO"] or termo in row["DESCRIÇÃO"] for termo in termos),
            axis=1,
        )

        resultados = df_base[filtro]

        if not resultados.empty:
            st.success(f"{len(resultados)} ITEM(NS) ENCONTRADO(S).")
            st.dataframe(resultados, use_container_width=True)
