"""Exceções customizadas do sistema."""


class GGMException(Exception):
    """Exceção base para erros do GGM."""
    pass


class DadosInsuficientesError(GGMException):
    """Levantada quando não há dados suficientes para análise."""
    pass


class SemDividendosError(GGMException):
    """Levantada quando a ação não paga dividendos."""
    pass


class ModeloInvalidoError(GGMException):
    """Levantada quando os parâmetros do modelo são inválidos."""
    pass


class PrecoIndisponivelError(GGMException):
    """Levantada quando não é possível obter o preço da ação."""
    pass