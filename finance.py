def calcular_retornos(dy, crescimento, anos):
    return sum([(dy * (1 + crescimento) ** i) / ((1 + crescimento) ** i) for i in range(1, anos + 1)])

def calcular_capm(taxa_livre, beta, premio_mercado):
    return taxa_livre + beta * premio_mercado