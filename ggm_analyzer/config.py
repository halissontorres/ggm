"""Configurações e constantes do sistema."""

from dataclasses import dataclass
from typing import Final


# Constantes do mercado brasileiro
TAXA_SELIC_PADRAO: Final[float] = 0.149
PREMIO_RISCO_BR_PADRAO: Final[float] = 0.065
TAXA_CRESCIMENTO_PADRAO: Final[float] = 0.03

# Limites de validação
CRESCIMENTO_MAXIMO: Final[float] = 0.15
CRESCIMENTO_MINIMO: Final[float] = -0.05
SPREAD_MINIMO: Final[float] = 0.02
MARGEM_SEGURANCA_MINIMA: Final[float] = 0.10

# Configurações de análise
ANOS_HISTORICO_PADRAO: Final[int] = 7
PERIODO_DIVIDENDOS: Final[str] = '12M'


@dataclass(frozen=True)
class ConfiguracaoGGM:
    """Configuração global do analisador GGM."""
    taxa_selic: float = TAXA_SELIC_PADRAO
    premio_risco_br: float = PREMIO_RISCO_BR_PADRAO
    anos_historico: int = ANOS_HISTORICO_PADRAO
    margem_seguranca_min: float = MARGEM_SEGURANCA_MINIMA
    
    def __post_init__(self):
        if self.taxa_selic < 0:
            raise ValueError("Taxa Selic não pode ser negativa")
        if self.premio_risco_br < 0:
            raise ValueError("Prêmio de risco não pode ser negativo")