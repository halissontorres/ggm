"""Calculadoras específicas para métricas financeiras."""

import pandas as pd
import warnings
from typing import Optional

from .config import (
    TAXA_CRESCIMENTO_PADRAO, CRESCIMENTO_MAXIMO, CRESCIMENTO_MINIMO
)


class CalculadoraCAPM:
    """Calcula a taxa de desconto via CAPM."""
    
    @staticmethod
    def calcular(
        taxa_livre_risco: float,
        beta: float,
        premio_risco_mercado: float
    ) -> float:
        """
        Calcula k = Rf + β * (Rm - Rf)
        
        Args:
            taxa_livre_risco: Taxa Selic ou título público
            beta: Sensibilidade da ação ao mercado
            premio_risco_mercado: Prêmio de risco do equity
        
        Returns:
            Taxa de desconto esperada
        """
        return taxa_livre_risco + beta * premio_risco_mercado


class CalculadoraCrescimento:
    """Calcula a taxa de crescimento perpétuo (g)."""
    
    @staticmethod
    def calcular_cagr(dividendos_anuais: pd.Series) -> Optional[float]:
        """
        Calcula CAGR dos dividendos.
        
        Args:
            dividendos_anuais: Série temporal de dividendos anuais
        
        Returns:
            Taxa de crescimento composta ou None se insuficiente
        """
        # Remove anos sem dividendos
        div_validos = dividendos_anuais[dividendos_anuais > 0]
        
        if len(div_validos) < 2:
            return None
        
        anos = len(div_validos) - 1
        g = (div_validos.iloc[-1] / div_validos.iloc[0]) ** (1 / anos) - 1
        
        # Validação e limitação
        if g > CRESCIMENTO_MAXIMO:
            warnings.warn(
                f"g muito alto ({g*100:.1f}%). Limitando a {CRESCIMENTO_MAXIMO*100:.0f}%"
            )
            g = CRESCIMENTO_MAXIMO
        elif g < CRESCIMENTO_MINIMO:
            warnings.warn(
                f"g negativo ({g*100:.1f}%). Usando g = 0%"
            )
            g = 0.0
        
        return g
    
    @classmethod
    def calcular_de_historico(
        cls,
        historico_dividendos: pd.Series
    ) -> float:
        """
        Calcula g a partir do histórico completo de dividendos.
        
        Args:
            historico_dividendos: Série temporal de dividendos
        
        Returns:
            Taxa de crescimento
        """
        # Agrupa por ano
        div_anual = historico_dividendos.resample('YE').sum()
        
        g = cls.calcular_cagr(div_anual)
        
        if g is None:
            warnings.warn(
                f"Poucos anos com dividendos. Usando g padrão = {TAXA_CRESCIMENTO_PADRAO*100:.0f}%"
            )
            return TAXA_CRESCIMENTO_PADRAO
        
        print(f"✓ g calculado (CAGR {len(div_anual)-1} anos): {g*100:.2f}%")
        return g


class CalculadoraGGM:
    """Calcula o preço justo via Gordon Growth Model."""
    
    @staticmethod
    def calcular_preco_justo(
        dividendo_atual: float,
        taxa_crescimento: float,
        taxa_desconto: float
    ) -> float:
        """
        Calcula: P = D₁ / (k - g) onde D₁ = D₀ * (1 + g)
        
        Args:
            dividendo_atual: D₀
            taxa_crescimento: g
            taxa_desconto: k
        
        Returns:
            Preço justo da ação
        """
        d1 = dividendo_atual * (1 + taxa_crescimento)
        return d1 / (taxa_desconto - taxa_crescimento)