import requests
from bs4 import BeautifulSoup
import pandas as pd
import logging

logger = logging.getLogger(__name__)

# Define o user agent para simular um navegador
agent = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

class Dividendo:
    def __init__(self, ticker):
        self.ticker = ticker

    def pegar_dividendos_acao(self):
        logger.info(f"Iniciando coleta de proventos para {self.ticker}")
        url = f"https://www.fundamentus.com.br/proventos.php?papel={self.ticker}"
        webpage = requests.get(url, headers=agent)
        
        soup = BeautifulSoup(webpage.content, "html.parser")
        resultados = soup.find(id="resultado")
        
        # Retorna DataFrame vazio se não encontrar resultados
        if not resultados:
                logger.info(f"Nenhum provento encontrado para {self.ticker}")
                return pd.DataFrame(columns=["papel", "data_com", "valor_provento", "tipo_provento", "data_pagamento", "por_quantas_acoes"])
            
        tabela_body = resultados.find("tbody")
        if not tabela_body:
                logger.info(f"Tabela de proventos vazia para {self.ticker}")
                return pd.DataFrame(columns=["papel", "data_com", "valor_provento", "tipo_provento", "data_pagamento", "por_quantas_acoes"])
            
        linhas = tabela_body.find_all("tr")
        logger.info(f"Encontradas {len(linhas)} linhas de proventos")
        
        data = []
        for linha in linhas:
                colunas = linha.find_all("td")
                valores = [ele.text.strip().replace(',', '.') for ele in colunas]
                if len(valores) == 5:
                    # Adiciona o ticker como primeira coluna
                    valores.insert(0, self.ticker)
                    data.append(valores)
                
        df = pd.DataFrame(data, columns=["papel", "data_com", "valor_provento", "tipo_provento", "data_pagamento", "por_quantas_acoes"])
        return df        
        return pd.DataFrame()