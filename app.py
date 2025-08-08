import streamlit as st
import pandas as pd

# Título e descrição
st.markdown("<div style='text-align: center; font-size: 14px;'>Desenvolvido por Victor von Glehn - Especialista de Engenharia Agrícola</div>", unsafe_allow_html=True)
st.image("logo_aroeira.png", width=120)

st.markdown("<h1 style='text-align: center;'>Pesquisa de Itens - Bioenergética Aroeira</h1>", unsafe_allow_html=True)

# Campo de entrada
st.write("Digite os códigos ou palavras separadas por vírgula ou enter:")
entrada = st.text_area("", height=60)
botao = st.button("Buscar")

# Tentativa de leitura da planilha
try:
    df = pd.read_excel("Pesquisa de itens.xlsm")

    # Remove a primeira coluna se ela for de índice automático (0, 1, 2...)
    if df.columns[0].lower() in ["", "unnamed: 0", "índice", "index"] or df.columns[0] == df.index.name:
        df = df.iloc[:, 1:]

    # Padronizar colunas para MAIÚSCULAS
    df.columns = df.columns.str.upper()

    # Formatar a coluna de R$ MÉDIO (caso exista)
    if "R$ MÉDIO" in df.columns:
        df["R$ MÉDIO"] = df["R$ MÉDIO"].apply(lambda x: f"R$ {x:.2f}" if pd.notna(x) else "-")

    # Quando o botão é pressionado
    if botao:
        termos = [termo.strip().lower() for termo in entrada.replace("\n", ",").split(",") if termo.strip() != ""]

        if not termos:
            st.warning("Digite pelo menos um termo para buscar.")
        else:
            resultado = df[
                df.apply(lambda row: any(
                    termo in str(row[campo]).lower()
                    for termo in termos
                    for campo in ["CÓDIGO", "DESCRICAO", "DESCRIÇÃO", "DESCRIÇÃO REDUZIDA", "DESCRIÇÃO ANTIGA"]
                    if campo in df.columns
                ), axis=1)
            ]

            if not resultado.empty:
                st.success(f"{len(resultado)} item(ns) encontrado(s).")
                st.dataframe(resultado, use_container_width=True)
            else:
                st.warning("Nenhum item encontrado.")

except FileNotFoundError:
    st.error("Erro ao carregar planilha: Arquivo 'Pesquisa de itens.xlsm' não encontrado.")
except Exception as e:
    st.error(f"Erro ao processar a planilha: {e}")
