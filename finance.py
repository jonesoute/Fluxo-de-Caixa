def calcular_capm(taxa_livre, beta, premio_mercado):
    """
    Calcula o retorno exigido usando o modelo CAPM.
    """
    return taxa_livre + beta * premio_mercado

def calcular_fluxo_caixa(dividendo, crescimento, anos, taxa_desconto):
    """
    Calcula o valor presente dos dividendos futuros projetados.
    """
    fluxo_total = 0
    for t in range(1, anos + 1):
        dividendo_t = dividendo * ((1 + crescimento) ** t)
        valor_presente = dividendo_t / ((1 + taxa_desconto) ** t)
        fluxo_total += valor_presente
    return fluxo_total
