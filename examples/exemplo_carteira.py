"""Exemplo de análise de carteira."""

from ggm_analyzer import analisar_carteira

if __name__ == "__main__":
    carteira = [
        "POMO4.SA"
    ]
    
    df = analisar_carteira(carteira)
    print("\n📊 RANKING DE OPORTUNIDADES\n")
    print(df.to_string(index=False))
    
    # Exportar para CSV
    df.to_csv("analise_carteira.csv", index=False)