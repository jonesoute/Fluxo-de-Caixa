import streamlit as st
import yfinance as yf
from finance import calcular_capm, calcular_fluxo_caixa

st.set_page_config(page_title="Valuation por Dividendos", layout="centered")

st.title("📊 Valuation por Fluxo de Dividendos")

with st.form("formulario"):
    ticker = st.text_input("Ticker da Ação", value="PETR4")
    dividendo = st.number_input("Valor do Dividendo Atual (R$)", value=3.5)
    dy_atual = st.number_input("Dividend Yield Atual (%)", value=17.75) / 100
    crescimento = st.number_input("Crescimento dos Dividendos (%)", value=4.0) / 100
    anos = st.number_input("Período de Análise (anos)", value=10, step=1)

    taxa_livre = st.number_input("Taxa Livre de Risco (Selic, %)", value=13.65) / 100
    premio_risco = st.number_input("Prêmio pelo Risco de Mercado (%)", value=5.0) / 100

    enviar = st.form_submit_button("Calcular Valuation")

if enviar:
    try:
        acao = yf.Ticker(ticker + ".SA")
        preco_atual = acao.history(period="1d")["Close"].iloc[-1]
        beta = acao.info.get("beta", 1)

        capm = calcular_capm(taxa_livre, beta, premio_risco)
        preco_justo = calcular_fluxo_caixa(dividendo, crescimento, anos, capm)

        st.subheader("📌 Resultado da Avaliação")
        st.write(f"**Preço atual da ação:** R$ {preco_atual:.2f}")
        st.write(f"**Beta:** {beta}")
        st.write(f"**CAPM (retorno exigido):** {capm:.2%}")
        st.success(f"**💰 Preço Máximo Recomendado (Valuation): R$ {preco_justo:.2f}**")
    except Exception as e:
        st.error(f"Erro ao obter dados: {e}")
