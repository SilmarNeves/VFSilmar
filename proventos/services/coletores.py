import requests
from bs4 import BeautifulSoup
from ..models import ProventoAcao
from datetime import datetime

class ColetorDividendos:
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
            
            for linha in linhas:
                colunas = linha.find_all("td")
                valores = [ele.text.strip() for ele in colunas]
                
                if len(valores) >= 5:
                    data_com = datetime.strptime(valores[0], '%d/%m/%Y') if valores[0] != '-' else None
                    valor_provento = float(valores[1].replace(',', '.'))
                    tipo_provento = valores[2]
                    data_pagamento = datetime.strptime(valores[3], '%d/%m/%Y') if valores[3] and valores[3] != '-' else None
                    por_quantas_acoes = int(valores[4])
                    
                    # Verifica se já existe um provento com mesmos dados
                    provento_existente = ProventoAcao.objects.filter(
                        ativo=self.ticker,
                        data_com=data_com,
                        tipo_provento=tipo_provento,
                        valor_provento=valor_provento
                    ).exists()
                    
                    # Só cria se não existir
                    if not provento_existente:
                        ProventoAcao.objects.create(
                            ativo=self.ticker,
                            data_com=data_com,
                            data_pagamento=data_pagamento,
                            tipo_provento=tipo_provento,
                            valor_provento=valor_provento,
                            por_quantas_acoes=por_quantas_acoes
                        )
            return True
        except Exception as e:
            print(f"Erro ao obter dados da ação {self.ticker}: {e}")
            return False

def coletar_proventos(papeis):
    for papel in papeis:
        ColetorDividendos(papel).pegar_dividendos_acao()
