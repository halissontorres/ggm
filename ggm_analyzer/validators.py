"""Validadores de parâmetros e dados."""

import warnings
from .config import SPREAD_MINIMO
from .exceptions import ModeloInvalidoError


class ValidadorGGM:
    """Valida os parâmetros do modelo GGM."""

    @staticmethod
    def validar_taxa_desconto_crescimento(k: float, g: float) -> None:
        """
        Valida que k > g (condição fundamental do modelo).

        Raises:
            ModeloInvalidoError: Se k <= g
        """
        if k <= g:
            raise ModeloInvalidoError(
                f"Modelo inválido: k ({k * 100:.2f}%) deve ser maior que "
                f"g ({g * 100:.2f}%). Considere ajustar os parâmetros manualmente."
            )

        spread = k - g
        if spread < SPREAD_MINIMO:
            warnings.warn(
                f"Spread muito baixo ({spread * 100:.2f}%). "
                f"Resultado pode ser sensível a pequenas variações."
            )

    @staticmethod
    def validar_dividendo_positivo(dividendo: float, ticker: str) -> None:
        """Valida que o dividendo é positivo."""
        if dividendo <= 0:
            raise ValueError(
                f"Dividendo inválido para {ticker}: {dividendo}"
            )

    @staticmethod
    def validar_preco_positivo(preco: float, ticker: str) -> None:
        """Valida que o preço é positivo."""
        if preco <= 0:
            raise ValueError(
                f"Preço inválido para {ticker}: {preco}"
            )