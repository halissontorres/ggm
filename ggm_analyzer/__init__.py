"""
GGM Analyzer - Análise de preço justo via Modelo de Gordon.

Exemplo de uso:
    >>> from ggm_analyzer import analisar_acao
    >>> resultado = analisar_acao("BBAS3.SA")
    >>> print(resultado)
"""

from .models import ParametrosGGM, ResultadoGGM, Recomendacao
from .analyzer import AnalisadorGGM
from .portfolio import AnalisadorCarteira
from .exceptions import (
    GGMException,
    DadosInsuficientesError,
    SemDividendosError,
    ModeloInvalidoError,
    PrecoIndisponivelError
)

# API simplificada
def analisar_acao(
    ticker: str,
    g: float = None,
    k: float = None,
    verbose: bool = True
) -> ResultadoGGM:
    """Função helper para análise rápida."""
    params = ParametrosGGM(ticker=ticker, g=g, k=k)
    analisador = AnalisadorGGM(params)
    resultado = analisador.analisar()
    
    if verbose:
        print(resultado)
    
    return resultado


def analisar_carteira(tickers: list[str], **kwargs) -> 'pd.DataFrame':
    """Analisa múltiplas ações."""
    analisador = AnalisadorCarteira()
    return analisador.analisar(tickers, **kwargs)


__version__ = "1.0.0"
__all__ = [
    'analisar_acao',
    'analisar_carteira',
    'AnalisadorGGM',
    'AnalisadorCarteira',
    'ParametrosGGM',
    'ResultadoGGM',
    'Recomendacao',
]