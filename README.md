# 📈 Calculadora de Valuation - FCD

Este aplicativo web foi desenvolvido com Python e Streamlit para realizar avaliações de ações com base no modelo de **Fluxo de Caixa Descontado (FCD)**, incorporando parâmetros realistas de mercado como CAPM, Beta histórico e taxa livre de risco baseada na curva futura SELIC.

## 🚀 Funcionalidades

- Entrada de dados customizável: Ticker, DY, crescimento, anos e margem de segurança.
- Consulta automática do preço da ação (Yahoo Finance).
- Cálculo de Beta com base em covariância histórica da ação vs IBOV.
- Estimativa da taxa livre de risco futura (curva DI via API do Bacen).
- Cálculo completo de FCD com projeção de dividendos + valor residual (perpetuidade).
- Aplicação automática de margem de segurança ao valor justo.
- Avaliação com base em Upside/Downside.
- Tabela interativa com os retornos acumulados e anualizados (Ação, IBOV, SELIC).
- Expansor com projeção anual dos fluxos e valor justo acumulado.
- Análise de sensibilidade com três parâmetros (crescimento, desconto e DY).
- Botão "Nova Análise" que reinicia o app sem fechar a aba.

## 📦 Instalação

1. Clone este repositório:
```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
```

2. Instale os requisitos:
```bash
pip install -r requirements.txt
```

3. Execute a aplicação:
```bash
streamlit run main.py
```

## 🛠 Tecnologias utilizadas

- Python 3.8+
- Streamlit
- yfinance
- pandas
- numpy
- requests

## 📊 Exemplo

Veja como o app funciona em tempo real com base nas variáveis fornecidas pelo usuário e dados dinâmicos de mercado. Ideal para investidores que desejam uma visão racional e ajustada ao risco.

## 📄 Licença

MIT - sinta-se livre para modificar e compartilhar.
