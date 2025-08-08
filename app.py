import streamlit as st
import pandas as pd
from PIL import Image

# --- CONFIGURAÇÃO INICIAL ---
st.set_page_config(layout="wide")

# --- FUNÇÃO PARA FORMATAR CAMPOS NUMÉRICOS ---
def formatar_colunas(df):
    df.columns = [col.upper() for col in df.columns]
    if 'R$ MÉDIO' in df.columns:
        df['R$ MÉDIO'] = df['R$ MÉDIO'].apply(lambda x: f"R$ {x:,.2f}".replace(".", ","))
    return df

# --- LOGO CENTRALIZADO ---
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("logo_aroeira.png", width=120)

# --- TEXTO DESENVOLVIDO POR (com fonte menor) ---
st.markdown(
    "<p style='text-align:center; font-size:13px;'>Desenvolvido por Victor von Glehn - Especialista de Engenharia Agrícola</p>",
    unsafe_allow_html=True
)

# --- TÍTULO (com fonte menor e sem ícone) ---
st.markdown(
    "<h3 style='text-align:center;'>Pesquisa de Itens - Bioenergética Aroeira</h3>",
    unsafe_allow_html=True
)

# --- CAMPO DE ENTRADA ---
st.markdown("Digite os códigos ou palavras separadas por vírgula ou enter:")
entrada = st.text_area("", height=60)
btn = st.button("Buscar")

# --- LEITURA DA PLANILHA ---
try:
    df_base = pd.read_excel("Pesquisa de itens.xlsm", sheet_name=0, dtype=str)
    df_base = df_base.apply(lambda col: col.str.upper() if col.dtype == "object" else col)
except Exception as e:
    st.error(f"Erro ao carregar planilha: {e}")
    st.stop()

# --- BUSCA ---
if btn:
    termos = [t.strip().upper() for t in entrada.replace("\n", ",").split(",") if t.strip()]
    
    if not termos:
        st.warning("Digite ao menos um termo válido para pesquisa.")
    else:
        col_busca = ['CÓDIGO', 'DESCRIÇÃO']
        resultados = df_base[df_base[col_busca[0]].astype(str).isin(termos)]
        
        for termo in termos:
            filtro_parcial = df_base[col_busca[1]].str.contains(termo, na=False)
            resultados = pd.concat([resultados, df_base[filtro_parcial]])

        if resultados.empty:
            st.warning("Nenhum item encontrado.")
        else:
            resultados = resultados.drop_duplicates()
            resultados = formatar_colunas(resultados)

            st.success(f"{len(resultados)} ITEM(NS) ENCONTRADO(S).")

            st.dataframe(
                resultados.reset_index(drop=True),
                use_container_width=True
            )
