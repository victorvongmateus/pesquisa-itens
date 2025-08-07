import streamlit as st
import pandas as pd

# Configurações da página
st.set_page_config(page_title="Pesquisa de Itens - Bioenergética Aroeira", layout="wide")

# Logo
st.image("logo_aroeira.png", width=100)

# Título
st.markdown("<h1 style='color: #0C1C4A;'>🔍 Pesquisa de Itens - Bioenergética Aroeira</h1>", unsafe_allow_html=True)

# Entrada de texto
entrada = st.text_area("Digite os códigos ou palavras separadas por vírgula ou enter:", height=60)

# Botão de busca
if st.button("Buscar"):
    if not entrada.strip():
        st.warning("Digite ao menos um código ou palavra.")
    else:
        try:
            # Leitura da planilha
            df = pd.read_excel("Pesquisa de itens.xlsm", sheet_name="Planilha1")

            # Verificação da existência das colunas
            if "Código" not in df.columns or "Descrição" not in df.columns:
                st.error("Coluna 'Código' ou 'Descrição' não encontrada na planilha.")
            else:
                # Lista de termos (podem ser códigos ou palavras)
                lista_termos = [
                    termo.strip().lower()
                    for termo in entrada.replace(",", "\n").splitlines()
                    if termo.strip()
                ]

                # Filtro por códigos ou palavras na descrição
                resultado = df[df["Código"].astype(str).isin(lista_termos) |
                               df["Descrição"].str.lower().str.contains('|'.join(lista_termos), na=False)]

                if resultado.empty:
                    st.warning("Nenhum item encontrado.")
                else:
                    st.success(f"{len(resultado)} item(ns) encontrado(s).")
                    st.dataframe(resultado.reset_index(drop=True), use_container_width=True)

        except FileNotFoundError:
            st.error("Arquivo da planilha não encontrado.")
        except Exception as e:
            st.error(f"Ocorreu um erro: {str(e)}")
