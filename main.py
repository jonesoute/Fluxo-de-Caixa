# main.py
import streamlit as st
import yfinance as yf

st.set_page_config(page_title="Valuation por FCD", layout="centered")
st.title("📈 Calculadora de Valuation - FCD")

with st.form("input_form"):
    ticker = st.text_input("Ticker da Ação (ex: PETR4.SA)", "PETR4.SA")
    dy = st.number_input("Dividend Yield Atual (ex: 0.08 para 8%)", min_value=0.0, max_value=1.0, value=0.08, format="%.4f")
    dividendo = st.number_input("Dividendo pago no último ano (R$)", min_value=0.0, value=3.50)
    crescimento = st.number_input("Crescimento anual dos dividendos (%)", min_value=0.0, max_value=1.0, value=0.04, format="%.4f")
    taxa_risco = st.number_input("Taxa Livre de Risco (ex: 0.11 para 11%)", min_value=0.0, max_value=1.0, value=0.11, format="%.4f")
    premio_mercado = st.number_input("Prêmio de Risco de Mercado (%)", min_value=0.0, max_value=1.0, value=0.05, format="%.4f")
    anos = st.slider("Período de análise (anos)", 1, 20, 10)
    incluir_residual = st.checkbox("Incluir valor residual (perpetuidade)?", value=True)
    enviar = st.form_submit_button("Calcular")

if enviar:
    with st.spinner("Calculando..."):
        try:
            ticker_obj = yf.Ticker(ticker)
            beta = ticker_obj.fast_info.get("beta")

            if beta is None:
                beta = 1.0  # fallback

            capm = taxa_risco + beta * premio_mercado
            fcd = 0

            for t in range(1, anos + 1):
                dividendo_projetado = dividendo * ((1 + crescimento) ** t)
                fcd += dividendo_projetado / ((1 + capm) ** t)

            # Valor residual (perpetuidade após os anos projetados)
            if incluir_residual:
                dividendo_final = dividendo * ((1 + crescimento) ** anos)
                valor_residual = (dividendo_final * (1 + crescimento)) / (capm - crescimento)
                valor_residual_descontado = valor_residual / ((1 + capm) ** anos)
                fcd += valor_residual_descontado
            else:
                valor_residual_descontado = 0

            st.success("Cálculo realizado com sucesso!")
            st.metric("Valor Justo por FCD (R$)", f"R$ {fcd:.2f}")
            st.caption(f"Beta: {beta:.4f} | CAPM: {capm:.4f} | Valor residual: R$ {valor_residual_descontado:.2f}")
        except Exception as e:
            st.error(f"Erro durante o cálculo: {str(e)}")
