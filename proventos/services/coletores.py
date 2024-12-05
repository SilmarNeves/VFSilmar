import requests
from bs4 import BeautifulSoup
import pandas as pd

class Dividendo:
    def __init__(self, ticker):
        self.ticker = ticker
   
    def pegar_dividendos_acao(self):
        agent = {
            "User-Agent": 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
        }
        url = f"https://www.fundamentus.com.br/proventos.php?papel={self.ticker}"
        webpage = requests.get(url, headers=agent)
        soup = BeautifulSoup(webpage.content, "html.parser")
        resultados = soup.find(id="resultado")

        try:
            tabela_body = resultados.find("tbody")
            linhas = tabela_body.find_all("tr")
        except AttributeError:
            return pd.DataFrame()

        data = []
        for linha in linhas:
            colunas = linha.find_all("td")
            colunas = [ele.text.strip().replace(',', '.') for ele in colunas]
            if len(colunas) == 5:
                data.append(colunas)

        return pd.DataFrame(data, columns=["Data_com", "data_pagamento", "tipo_provento", "valor_provento", "por_quantas_acoes"])

class FII:
    def __init__(self, ticker):
        self.ticker = ticker

    def pegar_dividendos_fii(self):
        agent = {
            "User-Agent": 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
        }
        url = f"https://www.fundamentus.com.br/fii_proventos.php?papel={self.ticker}&tipo=2"
        webpage = requests.get(url, headers=agent)
        soup = BeautifulSoup(webpage.content, "html.parser")
        resultados = soup.find(id="resultado")

        if resultados is None:
            return pd.DataFrame()

        tabela_body = resultados.find("tbody")
        linhas = tabela_body.find_all("tr")
        data = []
        for linha in linhas:
            colunas = linha.find_all("td")
            colunas = [ele.text.strip() for ele in colunas]
            data.append([ele for ele in colunas if ele])

        return pd.DataFrame(data, columns=["Data_com", "rendimento", "data_rendimento", "valor"])
