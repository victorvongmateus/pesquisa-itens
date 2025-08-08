import streamlit as st
import pandas as pd
from PIL import Image

# Configurações da página
st.set_page_config(page_title="Pesquisa de Itens – Bioenergética Aroeira", layout="wide")

# Carrega logo
logo = Image.open("logo_aroeira.png")

# Cabeçalho com logo à esquerda e título ao lado
col1, col2 = st.columns([1, 4])
with col1:
    st.image(logo, width=150)
with col2:
    st.markdown("<h1 style='margin-bottom: 0;'>Pesquisa de Itens – Bioenergética Aroeira</h1>", unsafe_allow_html=True)
    st.markdown("<b>Desenvolvido por Victor von Glehn Mateus</b>", unsafe_allow_html=True)

st.markdown("---")

# Campo de busca
termo_busca = st.text_input("Digite o termo ou código que deseja buscar:")

# Carregar base
@st.cache_data
def carregar_dados():
    df = pd.read_excel("Pesquisa de itens.xlsm", sheet_name="Base")
    return df

df_base = carregar_dados()
df_base.columns = df_base.columns.str.upper()

# Aplica filtro se houver termo
if termo_busca:
    termo = termo_busca.strip().lower()
    filtro = df_base.apply(lambda row: termo in str(row.get("CODIGO", "")).lower()
                                      or termo in str(row.get("DESCRICAO", "")).lower()
                                      or termo in str(row.get("DESCRIÇÃO ANTIGA", "")).lower(), axis=1)
    df_filtrado = df_base[filtro]
else:
    df_filtrado = pd.DataFrame()

# Exibe resultados
if not df_filtrado.empty:
    st.success(f"{len(df_filtrado)} item(ns) encontrado(s).")

    # Colunas desejadas
    colunas_exibir = ["CODIGO", "DESCRICAO", "DESCRIÇÃO ANTIGA", "SITUACAO", "MIN", "MAX", "R$ MÉDIO"]
    colunas_validas = [col for col in colunas_exibir if col in df_filtrado.columns]

    # Formatar R$ MÉDIO
    if "R$ MÉDIO" in df_filtrado.columns:
        df_filtrado["R$ MÉDIO"] = df_filtrado["R$ MÉDIO"].apply(
            lambda x: f"R$ {x:.2f}" if pd.notna(x) and isinstance(x, (int, float)) else "-"
        )

    st.dataframe(df_filtrado[colunas_validas], use_container_width=True, hide_index=True)
elif termo_busca:
    st.warning("Nenhum resultado encontrado.")
