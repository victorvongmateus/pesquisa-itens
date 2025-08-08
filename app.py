import streamlit as st
import pandas as pd
import base64

# Função para carregar a planilha
@st.cache_data
def carregar_planilha():
    try:
        xls = pd.ExcelFile('Pesquisa de itens.xlsm')
        df = pd.read_excel(xls, sheet_name=xls.sheet_names[0])
        return df
    except Exception as e:
        st.error(f"Erro ao carregar planilha: {e}")
        return None

# Função para converter imagem em base64
def get_image_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Página
st.set_page_config(page_title="Pesquisa de Itens - Bioenergética Aroeira", layout="wide")

# Logo
logo_base64 = get_image_base64("logo_aroeira.png")
st.markdown(
    f"""
    <div style="display: flex; align-items: center; justify-content: center;">
        <img src="data:image/png;base64,{logo_base64}" alt="Logo" style="height: 100px; margin-right: 30px;">
    </div>
    """,
    unsafe_allow_html=True
)

# Título e subtítulo
st.markdown("<p style='text-align: center; font-size: 14px;'>Desenvolvido por Victor von Glehn - Especialista de Engenharia Agrícola</p>", unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center;'>🔍 PESQUISA DE ITENS - BIOENERGÉTICA AROEIRA</h1>", unsafe_allow_html=True)

# Entrada
termo = st.text_area("Digite os códigos ou palavras separadas por vírgula ou enter:")

# Botão
if st.button("Buscar"):
    df = carregar_planilha()
    if df is not None:
        # Padronizar colunas
        df.columns = [col.upper() for col in df.columns]

        # Transformar coluna 'DESCRIÇÃO REDUZIDA' e outras em str maiúsculas
        for col in df.columns:
            if df[col].dtype == object:
                df[col] = df[col].astype(str).str.upper()

        # Corrigir nome das colunas e formatação R$
        if "R$ MÉDIO" in df.columns:
            df["R$ MÉDIO"] = df["R$ MÉDIO"].apply(lambda x: f"R$ {x:,.2f}" if pd.notnull(x) else "-")

        # Remover primeira coluna (oculta, índice antigo)
        if df.columns[0] not in ['CÓDIGO', 'CODIGO']:
            df = df.iloc[:, 1:]

        # Filtrar por termos
        termos = [t.strip().upper() for t in termo.replace("\n", ",").split(",") if t.strip()]
        resultado = df[df.apply(lambda row: any(t in str(row.values).upper() for t in termos), axis=1)]

        if not resultado.empty:
            st.success(f"{len(resultado)} ITEM(NS) ENCONTRADO(S).")
            st.dataframe(resultado)
        else:
            st.warning("Nenhum item encontrado.")
