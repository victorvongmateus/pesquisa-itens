import streamlit as st
import pandas as pd
import base64

# Função para converter imagem para base64
def get_base64_logo():
    with open("logo_aroeira.png", "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Carregar imagem em base64
logo_base64 = get_base64_logo()

# Exibir logo centralizada
st.markdown(
    f"""
    <div style='text-align: center;'>
        <img src='data:image/png;base64,{logo_base64}' width='130'>
    </div>
    """,
    unsafe_allow_html=True
)

# Título centralizado com fontes ajustadas
st.markdown(
    """
    <div style='text-align: center; font-size:14px; color: #444;'>Desenvolvido por Victor von Glehn - Especialista de Engenharia Agrícola</div>
    <h2 style='text-align: center; font-size:26px;'>Pesquisa de Itens - Bioenergética Aroeira</h2>
    """,
    unsafe_allow_html=True
)

# Entrada de busca
st.write("Digite os códigos ou palavras separadas por vírgula ou enter:")
entrada = st.text_area("", height=70)
buscar = st.button("Buscar")

# Carregamento da base de dados
@st.cache_data
def carregar_base():
    df = pd.read_excel("Pesquisa de itens.xlsm", sheet_name=0, dtype=str)
    df.columns = df.columns.str.upper()
    return df

df_base = carregar_base()

# Executar busca
if buscar:
    termos = [t.strip().upper() for t in entrada.replace('\n', ',').split(',') if t.strip() != ""]
    
    if termos:
        colunas_busca = ["CODIGO", "DESCRICAO"]
        df_filtrado = df_base[df_base[colunas_busca].apply(lambda row: any(t in str(v).upper() for t in termos for v in row), axis=1)]

        # Formatando valores
        if "R$ MEDIO" in df_filtrado.columns:
            df_filtrado["R$ MEDIO"] = df_filtrado["R$ MEDIO"].apply(lambda x: f"R$ {float(x):,.2f}".replace(".", ",") if x not in [None, "", "nan"] else "-")

        # Exibir resultado
        st.success(f"{len(df_filtrado)} ITEM(NS) ENCONTRADO(S).")
        st.dataframe(df_filtrado.reset_index(drop=True), use_container_width=True)
    else:
        st.warning("Digite pelo menos um termo para buscar.")
