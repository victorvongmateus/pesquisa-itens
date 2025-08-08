import streamlit as st
import pandas as pd
import base64

# --- Função para carregar e converter imagem para base64 ---
def get_base64_logo():
    with open("logo.png", "rb") as f:
        return base64.b64encode(f.read()).decode()

# --- Carregamento da imagem ---
logo_base64 = get_base64_logo()

# --- Centralizar logo e títulos ---
st.markdown(
    f"""
    <div style="text-align: center;">
        <img src="data:image/png;base64,{logo_base64}" width="120">
        <p style="font-size:13px; margin-top: 10px;">Desenvolvido por Victor von Glehn - Especialista de Engenharia Agrícola</p>
        <h2 style="margin-top: 5px; font-size: 26px;">Pesquisa de Itens - Bioenergética Aroeira</h2>
    </div>
    """,
    unsafe_allow_html=True
)

# --- Campo de entrada ---
st.write("Digite os códigos ou palavras separadas por vírgula ou enter:")
input_text = st.text_area("", height=80)
buscar = st.button("Buscar")

# --- Realizar a busca ---
if buscar:
    if not input_text.strip():
        st.warning("Por favor, insira ao menos um código ou palavra.")
    else:
        try:
            df_base = pd.read_excel("Pesquisa de itens.xlsm", sheet_name="Base")
            df_base.columns = [col.upper() for col in df_base.columns]

            termos = [t.strip().upper() for t in input_text.replace("\n", ",").split(",") if t.strip()]
            resultados = pd.DataFrame()

            for termo in termos:
                filtro = df_base["CÓDIGO"].astype(str).str.contains(termo) | df_base["DESCRIÇÃO"].str.upper().str.contains(termo)
                encontrados = df_base[filtro]
                resultados = pd.concat([resultados, encontrados])

            resultados.drop_duplicates(inplace=True)

            if not resultados.empty:
                st.success(f"{len(resultados)} ITEM(NS) ENCONTRADO(S).")
                # Remover a primeira coluna se ela for apenas índice antigo
                resultados.reset_index(drop=True, inplace=True)
                # Formatar coluna de preço
                if "R$ MÉDIO" in resultados.columns:
                    resultados["R$ MÉDIO"] = resultados["R$ MÉDIO"].apply(lambda x: f"R$ {x:,.2f}".replace(".", ",") if pd.notnull(x) else "-")
                # Substituir valores 0 por "-"
                for col in ["MÍN", "MÁX"]:
                    if col in resultados.columns:
                        resultados[col] = resultados[col].replace(0, "-")
                st.dataframe(resultados)
            else:
                st.warning("Nenhum item encontrado.")
        except Exception as e:
            st.error(f"Erro ao carregar planilha: {e}")
