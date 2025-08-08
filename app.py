import streamlit as st
import pandas as pd

# Configurações da página
st.set_page_config(page_title="Pesquisa de Itens - Bioenergética Aroeira", layout="wide")

# Texto acima
st.markdown("<div style='text-align: center; font-size: 14px;'>Desenvolvido por Victor von Glehn - Especialista de Engenharia Agrícola</div>", unsafe_allow_html=True)

# Logo da Aroeira
st.image("logo_aroeira.png", width=120)

# Título
st.markdown("<h1 style='text-align: center;'>🔍 Pesquisa de Itens - Bioenergética Aroeira</h1>", unsafe_allow_html=True)

# Campo de entrada
st.write("Digite os códigos ou palavras separadas por vírgula ou enter:")
entrada = st.text_area("", height=60)

# Botão de busca
if st.button("Buscar"):
    try:
        # Leitura da planilha
        df = pd.read_excel("Pesquisa de itens.xlsm", sheet_name="Planilha1", dtype=str)

        # Força todas as colunas para string
        df = df.astype(str)

        # Transforma todas as colunas em maiúsculas
        df.columns = df.columns.str.upper()

        # Aplica maiúsculas no conteúdo
        df = df.applymap(lambda x: x.upper())

        # Converte valor médio para float e formata com R$
        if "R$ MÉDIO" in df.columns:
            df["R$ MÉDIO"] = df["R$ MÉDIO"].replace("-", "0").str.replace(",", ".", regex=False).astype(float)
            df["R$ MÉDIO"] = df["R$ MÉDIO"].apply(lambda x: f"R$ {x:.2f}" if x > 0 else "-")

        # Divide termos por vírgula, quebra de linha ou espaço
        termos = [t.strip().upper() for t in entrada.replace("\n", ",").replace(" ", ",").split(",") if t.strip()]

        # Função para verificar se qualquer termo está presente
        def contem_termo(linha):
            return any(termo in linha for termo in termos)

        # Aplica filtro nas colunas principais
        colunas_busca = ["CÓDIGO", "DESCRIÇÃO"]
        resultado = df[df[colunas_busca].apply(lambda row: contem_termo(" ".join(row)), axis=1)]

        if not resultado.empty:
            st.success(f"{len(resultado)} ITEM(NS) ENCONTRADO(S).")

            # Oculta o índice e exibe resultado
            st.dataframe(resultado.reset_index(drop=True), use_container_width=True)
        else:
            st.warning("Nenhum item encontrado.")

    except Exception as e:
        st.error(f"Erro ao carregar planilha: {e}")
