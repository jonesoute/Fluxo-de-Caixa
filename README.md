📊 Valuation por Fluxo de Caixa Livre
Este é um aplicativo web desenvolvido com Python e Streamlit, que calcula o preço máximo recomendado para compra de uma ação com base na projeção de dividendos futuros e no modelo de valuation por fluxo de caixa descontado.

🧮 Como Funciona
O app utiliza os seguintes conceitos:

CAPM (Capital Asset Pricing Model) para calcular o retorno exigido

Modelo de Gordon ajustado para calcular o valor presente dos dividendos futuros

Busca automática de dados da ação (preço atual, beta) via API do yfinance

📝 Entradas do Usuário
Campo	Tipo	Descrição
Ticker	Texto	Código da ação (ex: PETR4)
Valor do Dividendo Atual	Numérico	Último dividendo anual pago (R$)
Dividend Yield Atual (%)	Percentual	DY atual com base no preço da ação
Crescimento dos Dividendos (%)	Percentual	Estimativa de crescimento anual dos dividendos
Período de Análise (anos)	Numérico	Quantos anos considerar na projeção (ex: 10)
Taxa Livre de Risco (%)	Percentual	Ex: SELIC atual
Prêmio pelo Risco de Mercado (%)	Percentual	Diferença entre mercado e livre de risco

🔁 Saídas Calculadas
Preço atual da ação (via API)

Beta da ação (via API)

CAPM: retorno exigido pelo investidor

💰 Preço máximo recomendado (valuation): quanto vale pagar pela ação com base nos dividendos futuros

🚀 Executando Localmente
1. Clone o repositório
bash
Copiar
Editar
git clone https://github.com/seu-usuario/valor-justo-dividendos.git
cd valor-justo-dividendos
2. Crie o ambiente virtual e ative:
bash
Copiar
Editar
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\\Scripts\\activate   # Windows
3. Instale as dependências:
bash
Copiar
Editar
pip install -r requirements.txt
4. Execute o app:
bash
Copiar
Editar
streamlit run main.py
🌐 Implantação na Nuvem (Streamlit Cloud)
Você pode publicar seu app gratuitamente em: https://streamlit.io/cloud

Faça login com sua conta GitHub

Conecte o repositório

Selecione main.py como arquivo principal

Clique em "Deploy"

📚 Tecnologias Usadas
Python 3.x

Streamlit

yfinance

Pandas & NumPy

📩 Licença
Este projeto está licenciado sob a MIT License. Sinta-se livre para usar e modificar.

