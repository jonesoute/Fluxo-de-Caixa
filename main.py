# main.py
import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import requests

def get_selic_futura(ano_final):
    try:
        response = requests.get("https://api.bcb.gov.br/dados/serie/bcdata.sgs.1178/dados/ultimos/20?formato=json")
        dados = response.json()
        for item in reversed(dados):
            if str(ano_final) in item['data']:
                return float(item['valor'].replace(',', '.')) / 100
        return float(dados[-1]['valor'].replace(',', '.')) / 100
    except:
        return 0.105  # fallback

st.set_page_config(page_title="Valuation por FCD", layout="centered")
st.title("📈 Calculadora de Valuation - FCD")

cols = st.columns([3, 2])
ticker = cols[0].text_input("Ticker da Ação (ex: PETR4)", "PETR4")
mostrar_preco = cols[1].empty()

if ticker:
    try:
        ticker_api = ticker + ".SA" if not ticker.endswith(".SA") else ticker
        preco_atual_preview = yf.Ticker(ticker_api).history(period="1d")["Close"].iloc[-1]
        mostrar_preco.metric("Preço da ação", f"R$ {preco_atual_preview:.2f}")
    except:
        mostrar_preco.warning("Ticker inválido ou sem dados recentes")

with st.form("input_form"):
    with st.expander("ℹ️ Entenda os campos de entrada"):
        st.markdown("""
        - **Dividend Yield Atual**: proporção de dividendos pagos em relação ao preço atual da ação.
        - **Crescimento dos Dividendos**: taxa de crescimento anual esperada dos dividendos.
        - **Período de Análise**: tempo considerado para o modelo de fluxo de caixa descontado.
        - **Margem de Segurança**: percentual de desconto aplicado sobre o valor justo calculado.
        """)
    dy = st.number_input("Dividend Yield Atual (ex: 0.08 para 8%)", min_value=0.0, max_value=1.0, value=0.08, format="%.4f")
    crescimento = st.number_input("Crescimento anual dos dividendos (%)", min_value=0.0, max_value=1.0, value=0.04, format="%.4f")
    anos = st.slider("Período de análise (anos)", 1, 20, 10)
    margem_segurança = st.number_input("Margem de segurança (%) aplicada ao valor justo", min_value=0.0, max_value=1.0, value=0.10, format="%.2f")
    enviar = st.form_submit_button("Calcular")

if enviar:
    with st.spinner("Calculando..."):
        try:
            if "dados" not in st.session_state:
                st.session_state["dados"] = {}
            ticker_api = ticker + ".SA" if not ticker.endswith(".SA") else ticker
            ticker_obj = yf.Ticker(ticker_api)
            preco_atual = ticker_obj.history(period="1d")["Close"].iloc[-1]

            ibov = yf.Ticker("^BVSP").history(period="1y")["Close"]
            acao = ticker_obj.history(period="1y")["Close"]
            df = pd.DataFrame({"acao": acao, "ibov": ibov}).dropna()
            df["ret_acao"] = df["acao"].pct_change()
            df["ret_ibov"] = df["ibov"].pct_change()
            df.dropna(inplace=True)

            cov = np.cov(df["ret_acao"], df["ret_ibov"])[0][1]
            var = np.var(df["ret_ibov"])
            beta = cov / var if var != 0 else 1.0

            ano_futuro = pd.Timestamp.today().year + anos
            taxa_risco = get_selic_futura(ano_futuro)
            retorno_mercado = ((1 + df["ret_ibov"].mean()) ** 252) - 1
            premio_mercado = retorno_mercado - taxa_risco
            capm = taxa_risco + beta * premio_mercado
            st.session_state["dados"] = {
                "capm": capm,
                "crescimento": crescimento,
                "dy": dy,
                "preco_atual": preco_atual,
                "dividendo": dividendo
            }
            dividendo = preco_atual * dy

            if capm > crescimento:
                fcd_fluxos = sum([(dividendo * (1 + crescimento) ** t) / (1 + capm) ** t for t in range(1, anos + 1)])
                valor_residual = ((dividendo * (1 + crescimento) ** (anos + 1)) / (capm - crescimento)) / (1 + capm) ** anos
                fcd_bruto = fcd_fluxos + valor_residual
                fcd_seguro = fcd_bruto * (1 - margem_segurança)
                upside = fcd_seguro - preco_atual
                upside_pct = (fcd_seguro / preco_atual) - 1
                avaliacao = "Upside" if upside > 0 else "Downside"
                mensagem = (
                    "O preço de mercado está abaixo do valor justo calculado"
                    if upside > 0 else
                    "O preço de mercado está acima do valor justo estimado"
                )

                retorno_acumulado_acao = (df['acao'].iloc[-1] / df['acao'].iloc[0]) - 1
                retorno_acumulado_ibov = (df['ibov'].iloc[-1] / df['ibov'].iloc[0]) - 1
                retorno_acumulado_selic = ((1 + taxa_risco) ** anos) - 1

                retorno_anual_acao = ((1 + retorno_acumulado_acao) ** (1 / anos)) - 1
                retorno_anual_ibov = ((1 + retorno_acumulado_ibov) ** (1 / anos)) - 1
                retorno_anual_selic = taxa_risco

                df_retornos = pd.DataFrame({
                    "Índice": ["Ação", "IBOV", "SELIC (aprox.)"],
                    "Retorno Acumulado": [retorno_acumulado_acao, retorno_acumulado_ibov, retorno_acumulado_selic],
                    "Retorno Anualizado": [retorno_anual_acao, retorno_anual_ibov, retorno_anual_selic]
                })
                st.subheader("📉 Retornos Históricos no Período")
                st.dataframe(df_retornos.style.format({"Retorno Acumulado": "{:.2%}", "Retorno Anualizado": "{:.2%}"}))
                st.caption(f"Estimado via curva DI futura para o ano {ano_futuro}")

                pl = preco_atual / dividendo if dividendo > 0 else "N/A"

                st.success("Cálculo realizado com sucesso!")
                st.metric("Valor Justo (FCD ajustado)", f"R$ {fcd_seguro:.2f}")
                st.caption(f" Prêmio de risco: {premio_mercado:.2%} | DY: {dy:.2%} | Beta calculado: {beta:.4f} | CAPM: {capm:.2%} | Dividendo: R$ {dividendo:.2f}")
                st.write(f"**{avaliacao} de {upside_pct:.2%}**")
                st.info(mensagem)
                st.write(f"**P/L estimado com base no dividendo:** {pl if pl == 'N/A' else f'{pl:.2f}'})")

                with st.expander("📋 Ver detalhes dos fluxos de dividendos"):
                    fluxo_tabela = []
                    acumulado = 0
                    for t in range(1, anos + 1):
                        div_proj = dividendo * (1 + crescimento) ** t
                        valor_desc = div_proj / (1 + capm) ** t
                        acumulado += valor_desc
                        fluxo_tabela.append({
                            "Ano": t,
                            "Dividendo Projetado": div_proj,
                            "Valor Presente": valor_desc,
                            "Valor Justo Acumulado": acumulado
                        })

                    fluxo_df = pd.DataFrame(fluxo_tabela)
                    fluxo_df["Dividendo Projetado"] = fluxo_df["Dividendo Projetado"].map("R$ {:.2f}".format)
                    fluxo_df["Valor Presente"] = fluxo_df["Valor Presente"].map("R$ {:.2f}".format)
                    fluxo_df["Valor Justo Acumulado"] = fluxo_df["Valor Justo Acumulado"].map("R$ {:.2f}".format)
                    st.table(fluxo_df)

                    st.markdown(f"**Valor residual ao final de {anos} anos:** R$ {valor_residual:.2f}")
                    st.markdown(f"**Valor justo total (sem margem):** R$ {fcd_bruto:.2f}")
                st.write(f"**P/L estimado com base no dividendo:** {pl if pl == 'N/A' else f'{pl:.2f}'}")

                st.subheader("📊 Análise de Sensibilidade Personalizada")
if "dados" in st.session_state:
    dados = st.session_state["dados"]
    capm = dados["capm"]
    crescimento = dados["crescimento"]
    dy = dados["dy"]
    preco_atual = dados["preco_atual"]
    dividendo = dados["dividendo"]

    st.markdown("""
**Como interpretar:**
- **Crescimento dos Dividendos**: simula como variações na expectativa de crescimento anual dos dividendos afetam o valor justo da ação.
- **Crescimento dos Dividendos (CAPM)**: simula diferentes percepções de risco, ajustando a taxa de desconto usada no modelo.
- **Dividend Yield**: simula variações na rentabilidade de dividendos em relação ao preço da ação.
""")
    simulacao = st.selectbox("Simular variações em:", ["Crescimento dos Dividendos", "Taxa de Desconto (CAPM)", "Dividend Yield"])
", "Dividend Yield"])

                cenarios = {
                    "Pessimista": -0.02,
                    "Neutro": 0,
                    "Otimista": 0.02
                }
                resultado = {}

                for nome, variacao in cenarios.items():
                    if simulacao == "Crescimento dos Dividendos":
                        cresc = crescimento + variacao
                        taxa = capm
                        valor = (dividendo * (1 + cresc)) / (taxa - cresc) if taxa > cresc else None
                    elif simulacao == "Taxa de Desconto (CAPM)":
                        cresc = crescimento
                        taxa = capm + variacao
                        valor = (dividendo * (1 + cresc)) / (taxa - cresc) if taxa > cresc else None
                    elif simulacao == "Dividend Yield":
                        dy_simulado = dy + variacao
                        div_sim = preco_atual * dy_simulado
                        valor = (div_sim * (1 + crescimento)) / (capm - crescimento) if capm > crescimento else None
                    else:
                        valor = None

                    resultado[nome] = f"R$ {valor:.2f}" if valor else "Inválido"

                st.write("**Cenários:**")
                st.table(pd.DataFrame(resultado.items(), columns=["Cenário", "Valor Justo Simulado"]))
            else:
                st.error("Erro: CAPM deve ser maior que o crescimento dos dividendos para o cálculo do FCD.")

        except Exception as e:
            st.error(f"Erro durante o cálculo: {str(e)}")
