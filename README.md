📈 Valuation por Fluxo de Caixa Descontado (FCD)
Este é um aplicativo web desenvolvido em Python com Streamlit para calcular o valor justo de ações com base no modelo de Fluxo de Caixa Descontado (FCD), utilizando dividendos projetados e dados históricos de mercado.

🧩 Funcionalidades
📌 Entrada de parâmetros manuais:

Ticker da ação
Dividend Yield atual
Crescimento anual dos dividendos
Taxa livre de risco
Prêmio de risco de mercado
Período de análise (anos)
Margem de segurança sobre o valor justo

📊 Cálculos automáticos:
Preço da ação via Yahoo Finance (visível ao digitar o ticker)
Beta calculado com base na covariância com o IBOVESPA
CAPM (retorno exigido)
Fluxo de Caixa Descontado com valor residual
Valor justo com aplicação de margem de segurança
Upside/Downside e avaliação final
Múltiplo estimado P/L com base nos dividendos

🧮 Análise de Sensibilidade:
Simulação de valor justo em cenários com diferentes taxas de crescimento e CAPM

📦 Requisitos
txt
Copiar
Editar
streamlit>=1.30.0
yfinance>=0.2.36
pandas>=2.0.3
numpy>=1.25.2
▶️ Como executar localmente
Clone o repositório:

bash
Copiar
Editar
git clone https://github.com/seu-usuario/valuation-fcd.git
cd valuation-fcd
(Opcional) Crie um ambiente virtual:

bash
Copiar
Editar
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\\Scripts\\activate   # Windows
Instale as dependências:

bash
Copiar
Editar
pip install -r requirements.txt
Execute o app:

bash
Copiar
Editar
streamlit run main.py
🧪 Exemplo de uso
Digite o ticker (ex: PETR4), informe os parâmetros como DY, crescimento dos dividendos e taxa Selic, e o app irá:

Calcular o beta com base no IBOV
Estimar o valor justo da ação via FCD
Exibir se há Upside ou Downside
Mostrar uma tabela de sensibilidade para diferentes cenários

🛠 Devcontainer (opcional)
Se estiver usando GitHub Codespaces ou VSCode com Docker, inclua o .devcontainer/devcontainer.json para configuração automática do ambiente.

📚 Tecnologias
Streamlit
yfinance
Pandas e NumPy
Python 3.11+

📄 Licença
Este projeto está licenciado sob a MIT License.
