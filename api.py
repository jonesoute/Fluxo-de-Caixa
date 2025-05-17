import yfinance as yf

def get_dados_acao(ticker):
    acao = yf.Ticker(ticker)
    hist = acao.history(period="1y")
    info = acao.info
    return {
        "preco_atual": info.get("currentPrice", 0),
        "beta": info.get("beta", 1.0),
        "dividendo_anual": info.get("dividendRate", 0),
        "hist": hist,
        "nome_empresa": info.get("shortName", ticker)
    }