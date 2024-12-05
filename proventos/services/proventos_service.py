from ..models import Provento
from .coletores import Dividendo, FII

def atualizar_proventos_acoes(codigos):
    resultados = []
    for codigo in codigos:
        dados = Dividendo(codigo).pegar_dividendos_acao()
        for _, row in dados.iterrows():
            provento = Provento.objects.create(
                papel=codigo,
                tipo_ativo='ACAO',
                data_com=row['Data_com'],
                valor=row['valor_provento'],
                tipo_provento=row['tipo_provento'],
                data_pagamento=row['data_pagamento']
            )
            resultados.append(provento)
    return resultados

def atualizar_proventos_fiis(codigos):
    resultados = []
    for codigo in codigos:
        dados = FII(codigo).pegar_dividendos_fii()
        for _, row in dados.iterrows():
            provento = Provento.objects.create(
                papel=codigo,
                tipo_ativo='FII',
                data_com=row['Data_com'],
                valor=row['valor'],
                tipo_provento=row['rendimento'],
                data_pagamento=row['data_rendimento']
            )
            resultados.append(provento)
    return resultados
