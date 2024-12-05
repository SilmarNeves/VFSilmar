from .atualizar_transacoes import atualizar_transacoes
from .gerar_portfolios import gerar_portfolios
from proventos.services.gerar_historico_portfolio import gerar_historico_portfolio
import logging

logger = logging.getLogger(__name__)

def atualizar_sistema():
    logger.info("Iniciando atualização do sistema...")
    
    # Passo 1: Atualizar transações e obter datas modificadas
    logger.info("Atualizando transações...")
    datas_atualizadas = atualizar_transacoes()
    
    # Passo 2: Gerar portfolios com as datas atualizadas
    logger.info("Gerando portfolios...")
    gerar_portfolios(datas_atualizadas)
    
    # Passo 3: Atualizar histórico do portfolio
    logger.info("Atualizando histórico do portfolio...")
    gerar_historico_portfolio(datas_atualizadas)
    
    logger.info("Atualização do sistema concluída com sucesso!")
    return True
