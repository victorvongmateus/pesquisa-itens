import streamlit as st
import pandas as pd
from PIL import Image
import unicodedata
import re
from io import BytesIO

st.set_page_config(page_title="Pesquisa de Itens – Bioenergética Aroeira", layout="wide")

# Carregar logo
logo = Image.open("logo_aroeira.png")

# Cabeçalho com logo à esquerda e título à direita
col1, col2 = st.columns([1, 6])
with col1:
    st.image(logo, width=150)
with col2:
    st.markdown("<h1 style='margin-bottom: 5px;'>Pesquisa de Itens – Bioenergética Aroeira</h1>", unsafe_allow_html=True)
    st.markdown("<b>Desenvolvido por Victor von Glehn – Especialista de Engenharia Agrícola</b>", unsafe_allow_html=True)

st.markdown("---")

# --------- Funções utilitárias ---------
def normalizar(txt: str) -> str:
    """Remove acentos, deixa minúsculo, remove pontuação e espaços extras."""
    if txt is None:
        return ""
    if not isinstance(txt, str):
        txt = str(txt)
    txt = unicodedata.normalize("NFKD", txt)
    txt = "".join(ch for ch in txt if not unicodedata.combining(ch))
    txt = txt.lower()
    txt = re.sub(r"[^a-z0-9]+", " ", txt)
    txt = re.sub(r"\s+", " ", txt).strip()
    return txt

def normalizar_serie(s: pd.Series) -> pd.Series:
    """Normalização vetorizada para ganhar performance."""
    return (
        s.fillna("")
         .astype(str)
         .map(normalizar)
    )

# Campo de busca
termo_busca = st.text_input("Digite o termo ou código que deseja buscar:")

# Carregar dados
@st.cache_data
def carregar_dados():
    # Leitura única da planilha
    df = pd.read_excel("Pesquisa de itens.xlsm", sheet_name="Base", engine="openpyxl")
    # Padroniza nomes de coluna
    df.columns = df.columns.str.strip().str.upper()

    # Seleciona apenas colunas que interessam (quando existirem)
    colunas_desejadas = ["CODIGO", "DESCRICAO", "DESCRIÇÃO ANTIGA", "SITUACAO", "MIN", "MAX", "R$ MÉDIO"]
    colunas_existentes = [c for c in colunas_desejadas if c in df.columns]
    df = df[colunas_existentes].copy()

    # Tipagem leve
    if "CODIGO" in df.columns:
        df["CODIGO"] = df["CODIGO"].astype(str)

    # --------- Índice de busca (pré-processado e vetorizado) ---------
    desc = normalizar_serie(df["DESCRICAO"]) if "DESCRICAO" in df.columns else pd.Series("", index=df.index)
    desc_ant = normalizar_serie(df["DESCRIÇÃO ANTIGA"]) if "DESCRIÇÃO ANTIGA" in df.columns else pd.Series("", index=df.index)
    cod = normalizar_serie(df["CODIGO"]) if "CODIGO" in df.columns else pd.Series("", index=df.index)

    df["_SEARCH_TEXT"] = (desc + " " + desc_ant + " " + cod).str.strip()

    return df

df_base = carregar_dados()

# Busca (totalmente vetorizada com str.contains e regex=False)
if termo_busca:
    termo_norm = normalizar(termo_busca)
    tokens = [t for t in termo_norm.split() if t]
    if tokens:
        mask = pd.Series(True, index=df_base.index)
        s = df_base["_SEARCH_TEXT"]
        for tok in tokens:
            # regex=False é mais rápido e seguro, pois já normalizamos (apenas [a-z0-9])
            mask &= s.str.contains(tok, regex=False)
        df_filtrado = df_base.loc[mask].drop(columns=["_SEARCH_TEXT"])
    else:
        df_filtrado = pd.DataFrame(columns=[c for c in df_base.columns if c != "_SEARCH_TEXT"])
else:
    df_filtrado = pd.DataFrame(columns=[c for c in df_base.columns if c != "_SEARCH_TEXT"])

# Formata R$ MÉDIO
if "R$ MÉDIO" in df_filtrado.columns and not df_filtrado.empty:
    valores = pd.to_numeric(df_filtrado["R$ MÉDIO"], errors="coerce")
    df_filtrado["R$ MÉDIO"] = valores.apply(
        lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".") if pd.notnull(x) else "-"
    )

# Resultados + Exportação
if termo_busca:
    if not df_filtrado.empty:
        st.success(f"{len(df_filtrado)} item(ns) encontrado(s).")
        st.dataframe(df_filtrado.reset_index(drop=True), use_container_width=True, hide_index=True)

        # ------- Botão: Baixar resultados em Excel -------
        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
            df_filtrado.reset_index(drop=True).to_excel(writer, index=False, sheet_name="Resultados")
        buffer.seek(0)

        nome_arquivo = f"resultados_pesquisa_{(termo_norm if termo_busca else 'itens')}.xlsx"
        st.download_button(
            label="📥 Baixar resultados (Excel)",
            data=buffer,
            file_name=nome_arquivo,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
    else:
        st.warning("Nenhum resultado encontrado.")
