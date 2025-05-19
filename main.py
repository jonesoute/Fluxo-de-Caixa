# main.py
import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

st.set_page_config(page_title="Valuation por FCD", layout="centered")
st.title("📈 Calculadora de Valuation - FCD")

with st.form("input_form"):
    cols = st.columns([3, 2])
    ticker = cols[0].text_input("Ticker da Ação (ex: PETR4)", "PETR4")
    mostrar_preco = cols[1].empty()

    dy = st.number_input("Dividend Yield Atual (ex: 0.08 para 8%)", min_value=0.0, max_value=1.0, value=0.08, format="%.4f")
    crescimento = st.number_input("Crescimento anual dos dividendos (%)", min_value=0.0, max_value=1.0, value=0.04, format="%.4f")
    taxa_risco = st.number_input("Taxa Livre de Risco (ex: 0.11 para 11%)", min_value=0.0, max_value=1.0, value=0.11, format="%.4f")
    premio_mercado = st.number_input("Prêmio de Risco de Mercado (%)", min_value=0.0, max_value=1.0, value=0.05, format="%.4f")
    anos = st.slider("Período de análise (anos)", 1, 20, 10)
    margem_segurança = st.number_input("Margem de segurança (%) aplicada ao valor justo", min_value=0.0, max_value=1.0, value=0.10, format="%.2f")
    enviar = st.form_submit_button("Calcular")

if enviar:
    with st.spinner("Calculando..."):
        try:
            ticker_api = ticker + ".SA" if not ticker.endswith(".SA") else ticker
            ticker_obj = yf.Ticker(ticker_api)
            preco_atual = ticker_obj.history(period="1d")["Close"].iloc[-1]
            mostrar_preco.metric("Preço da ação", f"R$ {preco_atual:.2f}")

            # Calcular o beta com base no IBOV
            ibov = yf.Ticker("^BVSP").history(period="1y")["Close"]
            acao = ticker_obj.history(period="1y")["Close"]
            df = pd.DataFrame({"acao": acao, "ibov": ibov}).dropna()
            df["ret_acao"] = df["acao"].pct_change()
            df["ret_ibov"] = df["ibov"].pct_change()
            df.dropna(inplace=True)

            cov = np.cov(df["ret_acao"], df["ret_ibov"])[0][1]
            var = np.var(df["ret_ibov"])
            beta = cov / var if var != 0 else 1.0

            capm = taxa_risco + beta * premio_mercado
            dividendo = preco_atual * dy

            if capm > crescimento:
                fcd_bruto = (dividendo * (1 + crescimento)) / (capm - crescimento)
                fcd_seguro = fcd_bruto * (1 - margem_segurança)
                upside = fcd_seguro - preco_atual
                upside_pct = (fcd_seguro / preco_atual) - 1
                avaliacao = "Upside" if upside > 0 else "Downside"
                mensagem = (
                    "O preço de mercado está abaixo do valor justo calculado"
                    if upside > 0 else
                    "O preço de mercado está acima do valor justo estimado"
                )

                # Cálculo de múltiplos
                pl = preco_atual / dividendo if dividendo > 0 else "N/A"

                st.success("Cálculo realizado com sucesso!")
                st.metric("Valor Justo (FCD ajustado)", f"R$ {fcd_seguro:.2f}")
                st.caption(f"Preço atual: R$ {preco_atual:.2f} | DY: {dy:.2%} | Beta calculado: {beta:.4f} | CAPM: {capm:.4f}")
                st.write(f"**{avaliacao} de {upside_pct:.2%}**")
                st.info(mensagem)
                st.write(f"**P/L estimado com base no dividendo:** {pl if pl == 'N/A' else f'{pl:.2f}'}")

                # Análise de sensibilidade
                st.subheader("📊 Análise de Sensibilidade")
                st.write("Simulação do valor justo com diferentes taxas de crescimento e CAPM:")
                sens_df = pd.DataFrame(index=["+1%", "+2%", "+3%", "+4%"], columns=["CAPM 10%", "CAPM 12%", "CAPM 14%"])
                taxas_crescimento = [crescimento + x/100 for x in range(1, 5)]
                taxas_capm = [0.10, 0.12, 0.14]

                for i, cres in enumerate(taxas_crescimento):
                    for j, cap in enumerate(taxas_capm):
                        if cap > cres:
                            valor = (dividendo * (1 + cres)) / (cap - cres)
                            sens_df.iloc[i, j] = f"R$ {valor:.2f}"
                        else:
                            sens_df.iloc[i, j] = "Inválido"
                st.dataframe(sens_df)
            else:
                st.error("Erro: CAPM deve ser maior que o crescimento dos dividendos para o cálculo do FCD.")

        except Exception as e:
            st.error(f"Erro durante o cálculo: {str(e)}")
