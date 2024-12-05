
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
from django.db import connection
import concurrent.futures
from django.core.cache import cache
import logging

logger = logging.getLogger(__name__)
def get_ultimo_dia_util():
    hoje = datetime.now()
    
    # Se estiver dentro do horário de pregão (10h às 18h), usa o dia atual
    if 10 <= hoje.hour < 18:
        hoje = hoje.date()
    else:
        # Fora do horário de pregão, usa o dia anterior
        hoje = (hoje - timedelta(days=1)).date()
    
    # Ajusta para o último dia útil
    while hoje.weekday() in [5, 6]:  # 5=sábado, 6=domingo
        hoje = hoje - timedelta(days=1)
    
    return hoje

def get_dia_util_anterior(ultimo_dia_util):
        dia = ultimo_dia_util - timedelta(days=1)
    
        # Ajusta para o dia útil anterior
        while dia.weekday() in [5, 6]:  # 5=sábado, 6=domingo
            dia = dia - timedelta(days=1)
        
        return dia
def obter_preco(ativo, data=None):
    try:
        ticker_symbol = f"{ativo}.SA"
        ticker = yf.Ticker(ticker_symbol)
        
        if data:
            hist = ticker.history(start=data, end=data + timedelta(days=1))
            logger.info(f"Buscando preço histórico para {ativo} na data {data}")
        else:
            hist = ticker.history(period="1d")
            logger.info(f"Buscando preço atual para {ativo}")
        
        if not hist.empty:
            preco = round(hist['Close'][0], 2)
            logger.info(f"Preço obtido do yfinance para {ativo}: {preco} - Data: {data if data else 'atual'}")
            return preco
            
        logger.warning(f"Nenhum preço encontrado para {ativo} na data {data if data else 'atual'}")
        return 0.0
        
    except Exception as e:
        logger.error(f"Erro ao buscar preço para {ativo}: {str(e)}")
        return 0.0

def buscar_precos(ativos):
    ativos_precos = {}
    ativos_precos_anteriores = {}
    ultimo_dia_util = get_ultimo_dia_util()
    dia_util_anterior = get_dia_util_anterior(ultimo_dia_util)

    logger.info(f"""
    Buscando cotações:
    Último dia útil: {ultimo_dia_util} ({ultimo_dia_util.strftime('%A')})
    Dia útil anterior: {dia_util_anterior} ({dia_util_anterior.strftime('%A')})
    """)

    def obter_precos(ativo):
        preco_atual = obter_preco(ativo, data=ultimo_dia_util)
        preco_anterior = obter_preco(ativo, data=dia_util_anterior)
        
        logger.info(f"""
        Resultado para {ativo}:
        - Data Atual ({ultimo_dia_util}): R$ {preco_atual}
        - Data Anterior ({dia_util_anterior}): R$ {preco_anterior}
        - Variação: {((preco_atual - preco_anterior) / preco_anterior * 100):.2f}%
        """)
        
        return ativo, preco_atual, preco_anterior

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        results = executor.map(obter_precos, ativos)
    
    for ativo, preco_atual, preco_anterior in results:
        if preco_atual:
            ativos_precos[ativo] = preco_atual
        if preco_anterior:
            ativos_precos_anteriores[ativo] = preco_anterior
    
    return ativos_precos, ativos_precos_anteriores

def atualizar_cotacao_otimizado(debug=False):
    debug_info = []
    
    def log_debug(mensagem):
        if debug:
            debug_info.append(mensagem)
            print(mensagem)
    
    logger.info("Iniciando atualização de cotações...")
    tabelas_portfolio = ["portfolio_silmar", "portfolio_monica", "portfolio_consolidadas"]

    ultimo_dia_util = get_ultimo_dia_util()
    dia_anterior = get_dia_util_anterior(ultimo_dia_util)

    with connection.cursor() as cursor:
        for tabela in tabelas_portfolio:
            logger.info(f"Processando tabela: {tabela}")
            log_debug(f"Processando tabela: {tabela}")
            
            cursor.execute(f"SELECT Ativo, Quantidade, Tipo FROM {tabela}")
            ativos_info = cursor.fetchall()
            logger.info(f"Ativos encontrados: {len(ativos_info)}")
            log_debug(f"Ativos encontrados: {len(ativos_info)}")

            ativos_precos, ativos_precos_anteriores = buscar_precos([info[0] for info in ativos_info])
            logger.info(f"Preços obtidos: {len(ativos_precos)} atuais, {len(ativos_precos_anteriores)} anteriores")
            log_debug(f"Preços obtidos: {len(ativos_precos)} atuais, {len(ativos_precos_anteriores)} anteriores")

            patrimonio_por_tipo = {}
            total_geral = 0

            rows_to_update = []
            for ativo, quantidade, tipo in ativos_info:
                preco_atual = ativos_precos.get(ativo)
                preco_anterior = ativos_precos_anteriores.get(ativo)
                
                log_debug(f"\nBuscando preço histórico para {ativo} na data {ultimo_dia_util}")
                
                if preco_atual and preco_anterior:
                    patrimonio_atual = round(quantidade * preco_atual, 2)
                    if tipo not in patrimonio_por_tipo:
                        patrimonio_por_tipo[tipo] = 0
                    patrimonio_por_tipo[tipo] += patrimonio_atual
                    total_geral += patrimonio_atual

                    log_debug(f"Preço obtido do yfinance para {ativo}: {preco_atual:.2f} - Data: {ultimo_dia_util}")
                    
                    variacao = round(((preco_atual - preco_anterior) / preco_anterior) * 100, 2)
                    log_debug(f"""
        Resultado para {ativo}:
        - Data Atual ({ultimo_dia_util}): R$ {preco_atual:.2f}
        - Data Anterior ({dia_anterior}): R$ {preco_anterior:.2f}
        - Variação: {variacao:.2f}%
        """)

            for ativo, quantidade, tipo in ativos_info:
                preco_atual = ativos_precos.get(ativo)
                preco_anterior = ativos_precos_anteriores.get(ativo)
                if preco_atual is not None and preco_anterior is not None:
                    patrimonio_atual = round(quantidade * preco_atual, 2)
                    ganho_perda = round(((preco_atual - preco_anterior) / preco_anterior) * 100, 2)
                    diferenca = round((preco_atual - preco_anterior) * quantidade, 2)
                    
                    percentual_ativo = round((patrimonio_atual / patrimonio_por_tipo[tipo]) * 100, 2) if patrimonio_por_tipo[tipo] else 0
                    percentual_carteira = round((patrimonio_atual / total_geral) * 100, 2) if total_geral else 0

                    cursor.execute(f"SELECT \"Preço Médio\" FROM {tabela} WHERE Ativo = %s", (ativo,))
                    preco_medio = cursor.fetchone()[0]
                    
                    variacao_total = round(((preco_atual - preco_medio) / preco_medio) * 100, 2)

                    rows_to_update.append((preco_atual, preco_anterior, ganho_perda, diferenca, patrimonio_atual, percentual_ativo, percentual_carteira, variacao_total, ativo))

            cursor.executemany(f"""
                UPDATE {tabela}
                SET "Preço Atual" = %s, "Preço Anterior" = %s, "Ganho/Perda Hoje %" = %s, 
                    "Ganho/Perda Hoje R$" = %s, "Patrimônio Atual" = %s, "% Ativo" = %s, 
                    "% Carteira" = %s, "Variação Total %" = %s
                WHERE Ativo = %s
            """, rows_to_update)

    logger.info("Atualização de cotações concluída")
    log_debug("Atualização de cotações concluída")
    connection.commit()
    
    return debug_info
