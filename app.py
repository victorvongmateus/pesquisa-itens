# Botão
if st.button("Buscar"):
    df = carregar_planilha()
    if df is not None:
        # Remover colunas sem nome
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

        # Padronizar colunas
        df.columns = [col.upper() for col in df.columns]

        # Padronizar texto para maiúsculo
        for col in df.select_dtypes(include='object').columns:
            df[col] = df[col].astype(str).str.upper()

        # Formatar valores do campo R$ MÉDIO
        if "R$ MÉDIO" in df.columns:
            df["R$ MÉDIO"] = df["R$ MÉDIO"].apply(lambda x: f"R$ {x:,.2f}" if pd.notnull(x) else "-")

        # Termos de busca
        termos = [t.strip().upper() for t in termo.replace("\n", ",").split(",") if t.strip()]

        if termos:
            # Concatenar todas as colunas em uma única string por linha
            texto_unificado = df.astype(str).agg(" ".join, axis=1)

            # Juntar termos em expressão regex
            regex = "|".join([re.escape(t) for t in termos])

            # Filtrar com str.contains (muito mais rápido)
            resultado = df[texto_unificado.str.contains(regex, na=False)]

            if not resultado.empty:
                st.success(f"{len(resultado)} ITEM(NS) ENCONTRADO(S).")
                st.dataframe(resultado)
            else:
                st.warning("Nenhum item encontrado.")
        else:
            st.warning("Digite ao menos um termo.")
