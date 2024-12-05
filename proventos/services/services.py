from .models import Provento
from .coletores import Dividendo, FII

def atualizar_proventos_acoes(codigos):
    for codigo in codigos:
        dados = Dividendo(codigo).pegar_dividendos_acao()
        for _, row in dados.iterrows():
            Provento.objects.create(
                papel=codigo,
                tipo_ativo='ACAO',
                data_com=row['Data_com'],
                valor=row['valor_provento'],
                tipo_provento=row['tipo_provento'],
                data_pagamento=row['data_pagamento']
            )
