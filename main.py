import streamlit as st
from api import get_dados_acao
from finance import calcular_retornos, calcular_capm

st.set_page_config(page_title="Análise de Ações", layout="wide")
st.title("📊 Analisador de Ações - Modelo DFC")

ticker = st.text_input("Ticker da ação", value="PETR4.SA")
dy = st.number_input("Dividend Yield Atual (%)", min_value=0.0, value=10.0) / 100
crescimento = st.number_input("Crescimento dos Dividendos (%)", min_value=0.0, value=4.0) / 100
dividendo = st.number_input("Valor atual do dividendo (R$)", min_value=0.0, value=3.00)
anos = st.slider("Período de análise (anos)", min_value=1, max_value=20, value=10)
selic = st.number_input("Taxa livre de risco (Selic %)", min_value=0.0, value=13.65) / 100

if st.button("📥 Analisar"):
    dados = get_dados_acao(ticker)
    retorno = calcular_retornos(dy, crescimento, anos)
    capm = calcular_capm(selic, dados["beta"], 0.05)

    st.success(f"Preço Atual: R$ {dados['preco_atual']:.2f}")
    st.info(f"CAPM Estimado: {capm:.2%}")
    st.metric("Fluxo de Caixa Estimado (10 anos)", f"R$ {retorno:.2f}")