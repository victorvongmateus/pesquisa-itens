import streamlit as st
import pandas as pd
from PIL import Image
from io import BytesIO

st.set_page_config(page_title="Pesquisa de Itens – Bioenergética Aroeira", layout="wide")

logo = Image.open("logo_aroeira.png")

col1, col2 = st.columns([1, 6])
with col1:
    st.image(logo, width=150)
with col2:
    st.markdown("<h1 style='margin-bottom: 5px;'>Pesquisa de Itens – Bioenergética Aroeira</h1>", unsafe_allow_html=True)
    st.markdown("<b>Desenvolvido por Victor von Glehn – Especialista de Engenharia Agrícola</b>", unsafe_allow_html=True)

st.markdown("---")

termo_busca = st.text_input("Digite o termo ou código que deseja buscar:")

@st.cache_data
def carregar_dados():
    df = pd.read_excel("Pesquisa de itens.xlsm", sheet_name="Base", engine="openpyxl")
    df.columns = df.columns.str.strip().str.upper()
    return df

df_base = carregar_dados()

colunas_desejadas = ["CODIGO", "DESCRICAO", "DESCRIÇÃO ANTIGA", "SITUACAO", "MIN", "MAX", "R$ MÉDIO"]
colunas_existentes = [col for col in colunas_desejadas if col in df_base.columns]
df_base = df_base[colunas_existentes]

if termo_busca:
    termo = termo_busca.strip().lower()
    filtro = df_base.apply(
        lambda row: termo in str(row.get("DESCRICAO", "")).lower()
                 or termo in str(row.get("DESCRIÇÃO ANTIGA", "")).lower()
                 or termo in str(row.get("CODIGO", "")).lower(),
        axis=1
    )
    df_filtrado = df_base[filtro]
else:
    df_filtrado = pd.DataFrame(columns=df_base.columns)

if "R$ MÉDIO" in df_filtrado.columns and not df_filtrado.empty:
    df_filtrado["R$ MÉDIO"] = df_filtrado["R$ MÉDIO"].apply(
        lambda x: f"R$ {x:,.2f}" if pd.notnull(x) and isinstance(x, (int, float)) else "-"
    )

if termo_busca:
    if not df_filtrado.empty:
        st.success(f"{len(df_filtrado)} item(ns) encontrado(s).")
        st.dataframe(df_filtrado.reset_index(drop=True), use_container_width=True, hide_index=True)

        # Botão para exportar Excel
        output = BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            df_filtrado.to_excel(writer, index=False, sheet_name="Resultados")
        processed_data = output.getvalue()

        st.download_button(
            label="📥 Exportar para Excel",
            data=processed_data,
            file_name="resultados_pesquisa.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.warning("Nenhum resultado encontrado.")
