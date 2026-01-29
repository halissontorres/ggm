"""Modelos de dados e estruturas."""

from dataclasses import dataclass
from typing import Optional
from enum import Enum


class Recomendacao(Enum):
    """Níveis de recomendação de compra."""
    EXCELENTE = "[SUBVALORIZADA] - Excelente oportunidade"
    BOA = "[SUBVALORIZADA] - Boa margem de segurança"
    RAZOAVEL = "[Ligeiramente barata] - Margem pequena"
    JUSTA = "[JUSTA] - Próxima ao valor teórico"
    CARA = "[SOBREVALORIZADA] - Evitar compra"


@dataclass
class ParametrosGGM:
    """Parâmetros de entrada para o modelo GGM."""
    ticker: str
    g: Optional[float] = None
    k: Optional[float] = None
    taxa_selic: float = 0.149
    premio_risco_br: float = 0.065
    anos_historico: int = 7
    margem_seguranca_min: float = 0.10


@dataclass
class DadosAcao:
    """Dados coletados de uma ação."""
    ticker: str
    dividendo_anual: float
    preco_atual: float
    beta: float
    historico_dividendos: list[float]


@dataclass
class ResultadoGGM:
    """Resultado da análise GGM."""
    ticker: str
    dividendo_atual: float
    dividendo_projetado: float
    taxa_crescimento: float
    taxa_desconto: float
    preco_justo: float
    preco_mercado: float
    margem_seguranca: float
    recomendacao: Recomendacao
    
    @property
    def dividend_yield(self) -> float:
        """Calcula o dividend yield atual."""
        return (self.dividendo_atual / self.preco_mercado) * 100
    
    @property
    def spread(self) -> float:
        """Retorna o spread k-g."""
        return self.taxa_desconto - self.taxa_crescimento
    
    def __str__(self) -> str:
        return (
            f"\n{'='*60}\n"
            f"GORDON GROWTH MODEL - {self.ticker.upper()}\n"
            f"{'='*60}\n"
            f"Dividendo anual atual (D₀)    : R$ {self.dividendo_atual:.3f}\n"
            f"Dividendo esperado ano 1 (D₁) : R$ {self.dividendo_projetado:.3f}\n"
            f"Dividend Yield                : {self.dividend_yield:.2f}%\n"
            f"Crescimento perpétuo (g)      : {self.taxa_crescimento*100:.2f}%\n"
            f"Taxa de desconto (k)          : {self.taxa_desconto*100:.2f}%\n"
            f"Spread (k - g)                : {self.spread*100:.2f}%\n"
            f"─────────────────────────────────────────────────────────\n"
            f"Preço justo (GGM)             : R$ {self.preco_justo:.2f}\n"
            f"Preço de mercado              : R$ {self.preco_mercado:.2f}\n"
            f"Margem de segurança           : {self.margem_seguranca*100:+.1f}%\n"
            f"─────────────────────────────────────────────────────────\n"
            f"Recomendação: {self.recomendacao.value}\n"
            f"{'='*60}\n"
        )