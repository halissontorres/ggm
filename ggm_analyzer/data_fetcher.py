"""Responsável por coletar dados do yfinance."""

import yfinance as yf
import pandas as pd
from typing import Optional
import warnings

from .models import DadosAcao
from .exceptions import SemDividendosError, PrecoIndisponivelError


class DataFetcher:
    """Coleta dados de ações via yfinance."""
    
    def __init__(self, ticker: str):
        self.ticker = ticker
        self._acao: Optional[yf.Ticker] = None
        self._info: Optional[dict] = None
    
    @property
    def acao(self) -> yf.Ticker:
        """Lazy loading do ticker."""
        if self._acao is None:
            self._acao = yf.Ticker(self.ticker)
        return self._acao
    
    @property
    def info(self) -> dict:
        """Lazy loading das informações."""
        if self._info is None:
            self._info = self.acao.info
        return self._info
    
    def obter_dividendo_anual(self) -> float:
        """Obtém o dividendo anual (D₀)."""
        # Tenta obter do yfinance direto
        d0 = self.info.get('trailingAnnualDividendRate')
        
        if d0 is not None and d0 > 0:
            return float(d0)
        
        # Fallback: calcula dos últimos 12 meses
        print("⚠️  Calculando dividendos via histórico...")
        dividends = self.acao.dividends
        
        if dividends.empty:
            raise SemDividendosError(
                f"Ação {self.ticker} não possui histórico de dividendos"
            )
        
        d0 = dividends.last('12M').sum()
        
        if d0 == 0:
            raise SemDividendosError(
                f"Ação {self.ticker} não pagou dividendos nos últimos 12 meses"
            )
        
        return float(d0)
    
    def obter_preco_atual(self) -> float:
        """Obtém o preço atual da ação."""
        preco = self.info.get('currentPrice') or \
                self.info.get('regularMarketPreviousClose')
        
        if preco is None:
            raise PrecoIndisponivelError(
                f"Não foi possível obter preço para {self.ticker}"
            )
        
        return float(preco)
    
    def obter_beta(self) -> float:
        """Obtém o beta da ação."""
        beta = self.info.get('beta', 1.0)
        
        if beta is None:
            warnings.warn(f"Beta indisponível para {self.ticker}. Usando β=1.0")
            return 1.0
        
        return float(beta)
    
    def obter_historico_dividendos(self) -> pd.Series:
        """Obtém o histórico de dividendos."""
        dividends = self.acao.dividends
        
        if dividends.empty:
            raise SemDividendosError(
                f"Ação {self.ticker} não possui histórico de dividendos"
            )
        
        return dividends
    
    def coletar_dados(self) -> DadosAcao:
        """Coleta todos os dados necessários."""
        return DadosAcao(
            ticker=self.ticker,
            dividendo_anual=self.obter_dividendo_anual(),
            preco_atual=self.obter_preco_atual(),
            beta=self.obter_beta(),
            historico_dividendos=self.obter_historico_dividendos().tolist()
        )