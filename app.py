import streamlit as st
import pandas as pd
import base64

# Função para converter imagem em base64
def get_base64_logo():
    with open("logo.png", "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Função para carregar base
@st.cache_data
def carregar_dados():
    try:
        df = pd.read_excel("Pesquisa de itens.xlsm", sheet_name=None)
        for nome_aba, dados in df.items():
            if "CÓDIGO" in dados.columns.str.upper():
                return dados
        st.error("Coluna 'CÓDIGO' não encontrada em nenhuma aba.")
    except Exception as e:
        st.error(f"Erro ao carregar planilha: {e}")
        return pd.DataFrame()

# Conversão para base64 da imagem
logo_base64 = get_base64_logo()

# --- Layout Superior ---
st.markdown(
    f"""
    <div style='text-align: center; margin-top: -40px; margin-bottom: -30px;'>
        <img src='data:image/png;base64,{logo_base64}' width='150'><br>
        <p style='font-size:12px; color:#333; margin-top:-5px;'>Desenvolvido por Victor von Glehn - Especialista de Engenharia Agrícola</p>
        <h2 style='font-size:28px;'>Pesquisa de Itens - Bioenergética Aroeira</h2>
    </div>
    """,
    unsafe_allow_html=True
)

# --- Entrada de pesquisa ---
st.write("Digite os códigos ou palavras separadas por vírgula ou enter:")
entrada = st.text_area("", height=80)
df_base = carregar_dados()

# --- Botão ---
if st.button("Buscar"):
    if not entrada.strip():
        st.warning("Digite pelo menos um termo.")
    else:
        termos = [termo.strip().upper() for termo in entrada.replace("\n", ",").split(",") if termo.strip()]
        col_busca = df_base.columns.str.upper()

        # Padronização
        for col in col_busca:
            df_base[col] = df_base[col].astype(str).str.upper()

        # Filtragem
        resultados = df_base[df_base.apply(
            lambda row: any(termo in str(row[col]) for termo in termos for col in col_busca),
            axis=1
        )]

        if not resultados.empty:
            st.success(f"{len(resultados)} item(ns) encontrado(s).")

            # Conversão e formatação
            resultados["R$ MÉDIO"] = resultados["R$ MÉDIO"].apply(
                lambda x: f"R$ {x:.2f}" if pd.notna(x) and x != "-" else "-"
            )

            # Exibir com letras maiúsculas e colunas desejadas
            colunas_desejadas = ["CÓDIGO", "DESCRIÇÃO", "DESCRIÇÃO ANTIGA", "SITUAÇÃO", "UNIDADE", "MÍN", "MÁX", "R$ MÉDIO"]
            colunas_disponíveis = [col for col in colunas_desejadas if col in resultados.columns.str.upper()]
            resultados.columns = resultados.columns.str.upper()
            st.dataframe(resultados[colunas_disponíveis])
        else:
            st.warning("Nenhum item encontrado.")
