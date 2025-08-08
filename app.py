import streamlit as st
import pandas as pd
import base64

# Função para carregar e preparar a planilha
@st.cache_data
def carregar_dados():
    try:
        df = pd.read_excel("Pesquisa de itens.xlsm", sheet_name=0)
        df.columns = df.columns.str.upper()
        df = df.iloc[:, 1:]  # remove a primeira coluna
        if "R$ MÉDIO" in df.columns:
            df["R$ MÉDIO"] = pd.to_numeric(df["R$ MÉDIO"], errors="coerce").fillna(0)
            df["R$ MÉDIO"] = df["R$ MÉDIO"].map(lambda x: f"R$ {x:.2f}")
        return df
    except Exception as e:
        st.error(f"Erro ao carregar planilha: {e}")
        return pd.DataFrame()

# Função para filtrar os dados
def filtrar_dados(df, termos):
    if df.empty:
        return df
    termos = [t.strip().upper() for t in termos if t.strip()]
    resultado = df[df.apply(lambda row: row.astype(str).str.upper().str.contains('|'.join(termos)).any(), axis=1)]
    return resultado

# Layout da página
st.set_page_config(page_title="Pesquisa de Itens", layout="wide")

# Logo da empresa
st.markdown('<div style="text-align: center;">', unsafe_allow_html=True)
logo_path = "logo_aroeira.png"
with open(logo_path, "rb") as image_file:
    encoded = base64.b64encode(image_file.read()).decode()
st.markdown(
    f'<img src="data:image/png;base64,{encoded}" alt="Logo" width="150">',
    unsafe_allow_html=True
)
st.markdown('</div>', unsafe_allow_html=True)

# Título e subtítulo
st.markdown("<h1 style='text-align: center;'>🔍 PESQUISA DE ITENS - BIOENERGÉTICA AROEIRA</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Desenvolvido por Victor von Glehn - Especialista de Engenharia Agrícola</p>", unsafe_allow_html=True)

# Entrada do usuário
entrada = st.text_area("Digite os códigos ou palavras separadas por vírgula ou enter:")

# Botão de busca
if st.button("Buscar"):
    termos = entrada.replace("\n", ",").split(",")
    dados = carregar_dados()
    resultado = filtrar_dados(dados, termos)

    if not resultado.empty:
        st.success(f"{len(resultado)} ITEM(NS) ENCONTRADO(S).")
        st.dataframe(resultado.reset_index(drop=True), use_container_width=True)
    else:
        st.warning("Nenhum item encontrado para os termos pesquisados.")
