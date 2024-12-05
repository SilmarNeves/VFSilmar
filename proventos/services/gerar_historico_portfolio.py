from django.db import connection
import pandas as pd
from datetime import datetime, timedelta
from ..models import HistoricoPortfolio

def gerar_historico_portfolio(data_inicio=None):
    carteiras = {
        "transacoes_consolidadas": "Consolidada",
        "transacoes_silmar": "Silmar",
        "transacoes_monica": "Monica"
    }

    with connection.cursor() as cursor:
        for tabela_origem, nome_carteira in carteiras.items():
            # Adiciona condição de data se necessário
            data_condition = "AND Data >= %s" if data_inicio else ""
            params = [data_inicio] if data_inicio else []
            
            cursor.execute(f"""
                SELECT Data, Operacao, Ativo, Quantidade, Preço 
                FROM {tabela_origem}
                WHERE 1=1 {data_condition}
                ORDER BY Data
            """, params)
            
            transacoes = cursor.fetchall()
            if not transacoes:
                continue

            df_transacoes = pd.DataFrame(
                transacoes, 
                columns=['Data', 'Operacao', 'Ativo', 'Quantidade', 'Preco']
            )

            ativos_unicos = df_transacoes['Ativo'].unique()
            
            for ativo in ativos_unicos:
                df_ativo = df_transacoes[df_transacoes['Ativo'] == ativo].copy()
                tipo = 'Ação' if 'AÇÃO' in df_ativo['Operacao'].iloc[0] else 'FII'
                
                posicao_atual = 0
                custo_total = 0

                for _, row in df_ativo.iterrows():
                    quantidade = row['Quantidade']
                    if 'COMPRA' in row['Operacao']:
                        if 'COMPRA' in row['Operacao']:
                            custo_total += quantidade * row['Preco']
                            posicao_atual += quantidade
                        else:  # VENDA
                            if posicao_atual > 0:
                                # Ajustar para zerar corretamente a posição quando vende tudo
                                custo_total = custo_total * ((posicao_atual - quantidade) / posicao_atual) if posicao_atual > quantidade else 0
                                posicao_atual -= quantidade
                    if posicao_atual > 0:
                        preco_medio = custo_total / posicao_atual
                        valor_total = posicao_atual * preco_medio

                        HistoricoPortfolio.objects.update_or_create(
                            data=row['Data'],
                            ativo=ativo,
                            carteira=nome_carteira,
                            defaults={
                                'quantidade': posicao_atual,
                                'preco_medio': preco_medio,
                                'tipo': tipo,
                                'valor_total': valor_total
                            }
                        )

    return True

    return True