import streamlit as st
import requests

st.set_page_config(page_title="Valuation por FCD", layout="centered")
st.title("📈 Calculadora de Valuation - FCD")

with st.form("input_form"):
    ticker = st.text_input("Ticker da Ação (ex: PETR4.SA)", "PETR4.SA")
    dy = st.number_input("Dividend Yield Atual (ex: 0.08 para 8%)", min_value=0.0, max_value=1.0, value=0.08)
    dividendo = st.number_input("Dividendo pago no último ano (R$)", min_value=0.0, value=3.50)
    crescimento = st.number_input("Crescimento anual dos dividendos (%)", min_value=0.0, max_value=1.0, value=0.04)
    taxa_risco = st.number_input("Taxa Livre de Risco (ex: 0.11 para 11%)", min_value=0.0, max_value=1.0, value=0.11)
    premio_mercado = st.number_input("Prêmio de Risco de Mercado (%)", min_value=0.0, max_value=1.0, value=0.05)
    anos = st.slider("Período de análise (anos)", 1, 20, 10)
    enviar = st.form_submit_button("Calcular")

if enviar:
    with st.spinner("Calculando..."):
        payload = {
            "ticker": ticker,
            "dy": dy,
            "crescimento_dividendo": crescimento,
            "taxa_livre_risco": taxa_risco,
            "premio_risco_mercado": premio_mercado,
            "dividendos_ano": dividendo,
            "anos": anos,
        }
        response = requests.post("http://localhost:8000/calcular", json=payload)

        if response.status_code == 200:
            data = response.json()
            if "erro" in data:
                st.error(f"Erro: {data['erro']}")
            else:
                st.success("Cálculo realizado com sucesso!")
                st.metric("Valor Justo por FCD (R$)", f"R$ {data['fcd']:.2f}")
                st.caption(f"Beta: {data['beta']} | CAPM: {data['capm']}")
        else:
            st.error("Erro ao conectar com a API. Verifique se o servidor está rodando.")
