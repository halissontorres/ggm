"""Exemplo básico de uso."""

from ggm_analyzer import analisar_acao

if __name__ == "__main__":
    # Análise simples
    resultado = analisar_acao("BBAS3.SA")
    
    # Análise customizada
    resultado = analisar_acao(
        "PETR4.SA",
        g=0.05,  # 5% de crescimento
        k=0.14,  # 14% de desconto
        verbose=True
    )