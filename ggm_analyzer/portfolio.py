"""Análise de carteira de ações."""

import pandas as pd
from typing import List, Optional

from .models import ParametrosGGM, ResultadoGGM
from .analyzer import AnalisadorGGM


class AnalisadorCarteira:
    """Analisa múltiplas ações simultaneamente."""
    
    def __init__(self, params_base: Optional[ParametrosGGM] = None):
        self.params_base = params_base or ParametrosGGM(ticker="")
    
    def analisar(
        self,
        tickers: List[str],
        verbose: bool = False
    ) -> pd.DataFrame:
        """
        Analisa uma lista de ações.
        
        Args:
            tickers: Lista de códigos de ações
            verbose: Se True, imprime cada análise
        
        Returns:
            DataFrame com resultados comparativos
        """
        resultados = []
        
        for ticker in tickers:
            try:
                params = ParametrosGGM(
                    ticker=ticker,
                    g=self.params_base.g,
                    k=self.params_base.k,
                    taxa_selic=self.params_base.taxa_selic,
                    premio_risco_br=self.params_base.premio_risco_br,
                    anos_historico=self.params_base.anos_historico,
                    margem_seguranca_min=self.params_base.margem_seguranca_min
                )
                
                analisador = AnalisadorGGM(params)
                res = analisador.analisar()
                
                if verbose:
                    print(res)
                
                resultados.append({
                    'Ticker': res.ticker,
                    'Preço Atual': res.preco_mercado,
                    'Preço Justo': res.preco_justo,
                    'Margem (%)': res.margem_seguranca * 100,
                    'Div Yield (%)': res.dividend_yield,
                    'k (%)': res.taxa_desconto * 100,
                    'g (%)': res.taxa_crescimento * 100,
                    'Spread (%)': res.spread * 100,
                    'Recomendação': res.recomendacao.value
                })
                
            except Exception as e:
                print(f"❌ Erro em {ticker}: {e}")
        
        df = pd.DataFrame(resultados)
        return df.sort_values('Margem (%)', ascending=False)