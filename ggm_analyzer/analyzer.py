"""Analisador principal do GGM."""

from typing import Optional
import warnings

from .models import ParametrosGGM, ResultadoGGM, Recomendacao, DadosAcao
from .data_fetcher import DataFetcher
from .calculators import CalculadoraCAPM, CalculadoraCrescimento, CalculadoraGGM
from .validators import ValidadorGGM
from .config import TAXA_CRESCIMENTO_PADRAO


class AnalisadorGGM:
    """Analisador de preço justo usando o Modelo de Gordon."""
    
    def __init__(self, params: ParametrosGGM):
        self.params = params
        self.data_fetcher = DataFetcher(params.ticker)
        self.validador = ValidadorGGM()
    
    def calcular_taxa_desconto(self, dados: DadosAcao) -> float:
        """Calcula k via CAPM ou usa valor manual."""
        if self.params.k is not None:
            print(f"✓ k fornecido manualmente: {self.params.k*100:.2f}%")
            return self.params.k
        
        k = CalculadoraCAPM.calcular(
            taxa_livre_risco=self.params.taxa_selic,
            beta=dados.beta,
            premio_risco_mercado=self.params.premio_risco_br
        )
        
        print(
            f"✓ k calculado via CAPM: {k*100:.2f}% "
            f"(Rf={self.params.taxa_selic*100:.1f}%, β={dados.beta:.2f})"
        )
        
        return k
    
    def calcular_crescimento(self) -> float:
        """Calcula g via CAGR ou usa valor manual."""
        if self.params.g is not None:
            print(f"✓ g fornecido manualmente: {self.params.g*100:.2f}%")
            return self.params.g
        
        try:
            historico = self.data_fetcher.obter_historico_dividendos()
            return CalculadoraCrescimento.calcular_de_historico(historico)
        except Exception:
            warnings.warn(
                f"Erro ao calcular g. Usando padrão = {TAXA_CRESCIMENTO_PADRAO*100:.0f}%"
            )
            return TAXA_CRESCIMENTO_PADRAO
    
    def determinar_recomendacao(self, margem: float) -> Recomendacao:
        """Determina a recomendação baseada na margem."""
        if margem > 0.20:
            return Recomendacao.EXCELENTE
        elif margem > self.params.margem_seguranca_min:
            return Recomendacao.BOA
        elif margem > 0:
            return Recomendacao.RAZOAVEL
        elif margem > -0.10:
            return Recomendacao.JUSTA
        else:
            return Recomendacao.CARA
    
    def analisar(self) -> ResultadoGGM:
        """Executa a análise completa."""
        # 1. Coleta dados
        dados = self.data_fetcher.coletar_dados()
        
        # 2. Calcula parâmetros
        k = self.calcular_taxa_desconto(dados)
        g = self.calcular_crescimento()
        
        # 3. Valida modelo
        self.validador.validar_taxa_desconto_crescimento(k, g)
        self.validador.validar_dividendo_positivo(dados.dividendo_anual, dados.ticker)
        self.validador.validar_preco_positivo(dados.preco_atual, dados.ticker)
        
        # 4. Calcula preço justo
        preco_justo = CalculadoraGGM.calcular_preco_justo(
            dividendo_atual=dados.dividendo_anual,
            taxa_crescimento=g,
            taxa_desconto=k
        )
        
        # 5. Calcula margem e recomendação
        margem = (preco_justo / dados.preco_atual) - 1
        recomendacao = self.determinar_recomendacao(margem)
        
        # 6. Retorna resultado
        return ResultadoGGM(
            ticker=dados.ticker,
            dividendo_atual=dados.dividendo_anual,
            dividendo_projetado=dados.dividendo_anual * (1 + g),
            taxa_crescimento=g,
            taxa_desconto=k,
            preco_justo=preco_justo,
            preco_mercado=dados.preco_atual,
            margem_seguranca=margem,
            recomendacao=recomendacao
        )