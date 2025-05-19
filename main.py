# main.py
import streamlit as st
import yfinance as yf

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
    enviar = st.form_submit_button("Calcular")

if enviar:
    with st.spinner("Calculando..."):
        try:
            ticker_api = ticker + ".SA" if not ticker.endswith(".SA") else ticker
            ticker_obj = yf.Ticker(ticker_api)
            preco_atual = ticker_obj.history(period="1d")["Close"].iloc[-1]
            mostrar_preco.metric("Preço da ação", f"R$ {preco_atual:.2f}")

            beta = ticker_obj.fast_info.get("beta")
            if beta is None:
                beta = 1.0  # fallback

            capm = taxa_risco + beta * premio_mercado
            dividendo = preco_atual * dy

            if capm > crescimento:
                fcd = (dividendo * (1 + crescimento)) / (capm - crescimento)
                upside = fcd - preco_atual
                upside_pct = (fcd / preco_atual) - 1
                avaliacao = "Upside" if upside > 0 else "Downside"
                mensagem = (
                    "O preço de mercado está abaixo do valor justo calculado"
                    if upside > 0 else
                    "O preço de mercado está acima do valor justo estimado"
                )

                st.success("Cálculo realizado com sucesso!")
                st.metric("Valor Justo (FCD)", f"R$ {fcd:.2f}")
                st.caption(f"Preço atual: R$ {preco_atual:.2f} | DY: {dy:.2%} | Beta: {beta:.4f} | CAPM: {capm:.4f}")
                st.write(f"**{avaliacao} de {upside_pct:.2%}**")
                st.info(mensagem)
            else:
                st.error("Erro: CAPM deve ser maior que o crescimento dos dividendos para o cálculo do FCD.")

        except Exception as e:
            st.error(f"Erro durante o cálculo: {str(e)}")
