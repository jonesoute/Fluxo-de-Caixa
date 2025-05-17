# api.py
import yfinance as yf
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CotacaoInput(BaseModel):
    ticker: str
    dy: float
    crescimento_dividendo: float
    taxa_livre_risco: float
    premio_risco_mercado: float
    dividendos_ano: float
    anos: int

@app.post("/calcular")
def calcular_fcd(data: CotacaoInput):
    try:
        info = yf.Ticker(data.ticker).info
        beta = info.get("beta")

        if beta is None:
            return {"erro": "Não foi possível obter o Beta da ação."}

        capm = data.taxa_livre_risco + beta * data.premio_risco_mercado

        # Cálculo do fluxo de caixa descontado (FCD)
        fcd = 0
        for t in range(1, data.anos + 1):
            dividendo_projetado = data.dividendos_ano * ((1 + data.crescimento_dividendo) ** t)
            fcd += dividendo_projetado / ((1 + capm) ** t)

        return {
            "ticker": data.ticker,
            "beta": round(beta, 4),
            "capm": round(capm, 4),
            "fcd": round(fcd, 2),
        }
    except Exception as e:
        return {"erro": str(e)}
