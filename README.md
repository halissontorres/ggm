# GGM Analyzer

Análise de preço justo de ações brasileiras usando o Modelo de Gordon (Gordon Growth Model).

> **Não se trata de um modelo de investimento, mas sim uma ferramenta para estimar o preço justo de uma ação com base em suas projeções de dividendos e crescimento. É importante avaliar outras informações financeiras e não se basear exclusivamente no resultado do modelo.**

 ### **Fórmula do Gordon Growth Model (GGM)**

O preço justo (ou preço-teto) da ação é o valor presente dos dividendos futuros, assumindo crescimento perpétuo constante:
Preço Justo = Dividendo Esperado no Próximo Ano (D1) / (Taxa de Desconto Requerida (k) - Taxa de Crescimento Perpétuo dos Dividendos (g))
em que:

> `D1 = Dividendo Atual (D0) × (1 + g)`: Use a média de dividendos dos últimos 3-5 anos, ajustada por crescimento projetado (ex.: baseado em guidance da empresa ou crescimento médio do lucro nos últimos anos).
> - k (taxa de desconto): Custo de oportunidade ajustado ao risco. No Brasil 2026, uma fórmula simples é: Selic (15%) + Prêmio de Risco Equity (3-5% para Brasil) × Beta da Ação (medida de volatilidade; ex.: 1 para mercado médio, >1 para cíclicas como commodities). Isso dá k entre 12-20% tipicamente. Subtraia inflação (4,5%) se quiser taxa real, mas use nominal para consistência.
> - g: Crescimento sustentável dos dividendos (ex.: 2-5% ao ano para empresas maduras no Brasil, baseado em crescimento do PIB projetado ~2% + inflação, ou histórico da empresa). Deve ser < k para o modelo convergir.

> Condições para usar: `k > g` (senão, preço infinito). Aplique só em empresas com payout consistente (bancos, utilities, saneamento), como no Bazin.
Exemplo Prático (Hipotético, com Dados de uma Ação como BBAS3)
Suponha uma ação com:

> Dividendo médio anual atual `(D0) = R$ 2,50` (média 5 anos, líquido de impostos se aplicável).
- g = 3% (crescimento esperado, baseado em projeções de lucro).
- k = 12% (Selic 15% ajustada para baixo por ser empresa estável com beta 0,8 e prêmio 4%: 15% - inflação 4,5% + risco ajustado).

Então:

> `D1 = 2,50 × (1 + 0,03) = R$ 2,575`
> 
>  `Preço Justo = 2,575 / (0,12 - 0,03) = 2,575 / 0,09 = R$ 28,61`
> 
>  `Se a ação cotar a R$ 25,00: Compre (subvalorizada, yield projetado > k - g)`.
> 
>  `Se cotar a R$ 35,00: Evite (sobrevalorizada).`

- Compare com Bazin: No original, Preço-Teto = 2,50 / 0,06 = R$ 41,67 (mais otimista, pois ignora crescimento e usa k baixa).

## Instalação
```bash
pip install -r requirements.txt
```

## Uso Rápido

### Análise Individual
```python
from ggm_analyzer import analisar_acao

# Análise automática (calcula g e k)
analisar_acao("BBAS3.SA")

# Análise customizada
analisar_acao("ITUB4.SA", g=0.05, k=0.14)
```

### Análise de Carteira
```python
from ggm_analyzer import analisar_carteira

carteira = ["BBAS3.SA", "ITUB4.SA", "TAEE11.SA"]
df = analisar_carteira(carteira)
print(df)
```

## Output
```
============================================================
GORDON GROWTH MODEL - BBAS3.SA
============================================================
Dividendo anual atual (D₀)    : R$ 2.450
Dividendo esperado ano 1 (D₁) : R$ 2.523
Dividend Yield                : 4.25%
Crescimento perpétuo (g)      : 2.98%
Taxa de desconto (k)          : 15.40%
Spread (k - g)                : 12.42%
────────────────────────────────────────────────────────
Preço justo (GGM)             : R$ 20.33
Preço de mercado              : R$ 24.50
Margem de segurança           : -17.0%
────────────────────────────────────────────────────────
Recomendação: SOBREVALORIZADA - Evitar compra
============================================================
```

## Estrutura do Projeto
```
ggm_analyzer/
├── __init__.py           # API pública
├── models.py             # Dataclasses
├── analyzer.py           # Lógica principal
├── data_fetcher.py       # Coleta de dados
├── calculators.py        # CAPM, CAGR, GGM
├── validators.py         # Validações
├── portfolio.py          # Análise de carteira
├── exceptions.py         # Exceções customizadas
└── config.py             # Constantes

examples/
├── exemplo_basico.py
└── exemplo_carteira.py
```

## Parâmetros

- **ticker**: Código da ação (ex: "BBAS3.SA")
- **g**: Taxa de crescimento perpétuo (None = calcula via CAGR)
- **k**: Taxa de desconto (None = calcula via CAPM)
- **taxa_selic**: Taxa livre de risco (padrão: 14.9%)
- **premio_risco_br**: Prêmio de risco Brasil (padrão: 6.5%)

## Fórmula
```
Preço Justo = D₁ / (k - g)

onde:
  D₁ = D₀ × (1 + g)
  k = Rf + β × (Rm - Rf)
```

## Requisitos

- Python 3.10+
- yfinance
- pandas

