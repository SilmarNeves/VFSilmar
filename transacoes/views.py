from django.shortcuts import render
from django.db import connection
import pandas as pd
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
<<<<<<< HEAD
from django.http import JsonResponse
from Atualizar_Transacoes.services.atualizar_sistema import atualizar_sistema
=======
>>>>>>> 18c34b6243b7ecca8b79329a6c5b8cc51857778c

@login_required
def get_transacoes_context(request):
    tabelas_nomes = {
        'transacoes_consolidadas': 'Consolidada',
        'transacoes_silmar': 'Silmar',
        'transacoes_monica': 'Monica'
    }

    tabela_selecionada = request.GET.get('tabela', 'transacoes_consolidadas')
    
    if tabela_selecionada not in tabelas_nomes:
        tabela_selecionada = 'transacoes_consolidadas'
    
    dados_por_tipo = {}
    columns = ['Selecionar', 'Data', 'Operação', 'Ativo', 'Quantidade', 'Preço', 'Corretora', 'Corretagem', 'Taxas', 'Impostos', 'IRRF']
    
    with connection.cursor() as cursor:
        cursor.execute(f"""
            SELECT id, Data, Operacao, Ativo, Quantidade, Preço, 
                   'INTER DTVM LTDA' as Corretora,
                   0.00 as Corretagem,
                   0.00 as Taxas,
                   0.00 as Impostos,
                   0.00 as IRRF
            FROM {tabela_selecionada} 
            ORDER BY Data DESC""")
        dados = cursor.fetchall()
    
    table_data = [
        [
            f'<input type="checkbox" class="transaction-select" data-id="{dado[0]}">',
            dado[1].strftime('%d-%m-%Y'),
            dado[2],
            dado[3],
            f"{dado[4]:.0f}",
            f"R$ {dado[5]:.2f}",
            dado[6],
            f"R$ {dado[7]:.2f}",
            f"R$ {dado[8]:.2f}",
            f"R$ {dado[9]:.2f}",
            f"R$ {dado[10]:.2f}"
        ] for dado in dados
    ]

    grid_context = {
        'title': 'Transações',
        'columns': columns,
        'table_data': table_data
    }
    
    dados_por_tipo['Transações'] = grid_context

    return {
        'tabelas_nomes': tabelas_nomes,
        'tabela_selecionada': tabela_selecionada,
        'dados_por_tipo': dados_por_tipo
    }

@login_required
def transacoes_view(request):
    context = get_transacoes_context(request)
    return render(request, 'transacoes/transacoes.html', context)

@login_required
def export_transactions(request):
    tabela_selecionada = request.GET.get('tabela', 'transacoes_consolidadas')
    selected_ids = request.POST.getlist('selected_ids[]')
    data_inicio = request.POST.get('data_inicio')
    data_fim = request.POST.get('data_fim')
    
    with connection.cursor() as cursor:
        query_conditions = []
        query_params = []
        
        if selected_ids:
            placeholders = ','.join(['%s'] * len(selected_ids))
            query_conditions.append(f"id IN ({placeholders})")
            query_params.extend(selected_ids)
            
        if data_inicio and data_fim:
            query_conditions.append("Data BETWEEN %s AND %s")
            query_params.extend([data_inicio, data_fim])
            
        where_clause = " AND ".join(query_conditions) if query_conditions else "1=1"
        
        query = f"""
            SELECT 
                Data, 
                Operacao as Operacao_Completa,
                Ativo, 
                Quantidade,
                Preço,
                'INTER DTVM LTDA' as Corretora,
                0.00 as Corretagem,
                0.00 as Taxas,
                0.00 as Impostos,
                0.00 as IRRF
            FROM {tabela_selecionada}
            WHERE {where_clause}
            ORDER BY Data DESC
        """
        cursor.execute(query, query_params)
        dados = cursor.fetchall()

          # Criando DataFrame com as colunas na ordem correta
    df = pd.DataFrame(dados, columns=[
              'Data operação', 'Operacao_Completa', 'Código Ativo', 'Quantidade',
              'Preço unitário', 'Corretora', 'Corretagem', 'Taxas', 'Impostos', 'IRRF'
          ])

    df['Data operação'] = pd.to_datetime(df['Data operação']).dt.strftime('%d/%m/%Y')

    def get_categoria(operacao_completa):
              if 'AÇÃO' in operacao_completa:
                  return 'Ações'
              elif 'FII' in operacao_completa:
                  return 'Fundos imobiliários'
              elif 'ETF' in operacao_completa:
                  return 'ETF'
              elif 'BDR' in operacao_completa:
                  return "BDR"
              return 'Outros'

    df.insert(1, 'Categoria', df['Operacao_Completa'].apply(get_categoria))

    df['Operação C/V'] = df['Operacao_Completa'].apply(lambda x: 'C' if 'COMPRA' in x else 'V')
    
    # Definindo a ordem final das colunas
    ordem_colunas = [
        'Data operação', 'Categoria', 'Código Ativo', 'Operação C/V',
        'Quantidade', 'Preço unitário', 'Corretora', 'Corretagem',
        'Taxas', 'Impostos', 'IRRF'
    ]
    
    df = df[ordem_colunas]

    # Formatação dos valores
    df['Quantidade'] = df['Quantidade'].apply(lambda x: f'{float(x):.8f}'.replace('.', ','))
    colunas_monetarias = ['Preço unitário', 'Corretagem', 'Taxas', 'Impostos', 'IRRF']
    for coluna in colunas_monetarias:
        df[coluna] = df[coluna].apply(lambda x: f'{float(x):.2f}'.replace('.', ','))

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=transacoes_exportadas.xlsx'
    
    df.to_excel(response, index=False)
    return response
<<<<<<< HEAD



@login_required
def atualizar_sistema_view(request):
    try:
        atualizar_sistema()
        return JsonResponse({'status': 'success', 'message': 'Sistema atualizado com sucesso!'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
=======
>>>>>>> 18c34b6243b7ecca8b79329a6c5b8cc51857778c
