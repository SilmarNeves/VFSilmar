from django.shortcuts import render, redirect
<<<<<<< HEAD
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .services.gerar_historico_portfolio import gerar_historico_portfolio
from .models import HistoricoPortfolio

from django.contrib import messages


@login_required
def historico_portfolio_view(request):
    if request.method == 'POST':
        try:
            gerar_historico_portfolio()
            messages.success(request, 'Histórico atualizado com sucesso!')
        except Exception as e:
            messages.error(request, f'Erro ao atualizar histórico: {str(e)}')
        return redirect('proventos:historico')

    historico = HistoricoPortfolio.objects.all().order_by('-data', 'ativo')
    dados_por_tipo = {}
    columns = ['Data', 'Ativo', 'Tipo', 'Quantidade', 'Preço Médio', 'Valor Total', 'Carteira']
    
    table_data = [
        [
            item.data.strftime('%d/%m/%Y'),
            item.ativo,
            item.tipo,
            f"{item.quantidade}",
            f"R$ {item.preco_medio:.2f}",
            f"R$ {item.valor_total:.2f}",
            item.carteira
        ] for item in historico
    ]

    grid_context = {
        'title': 'Histórico do Portfólio',
        'columns': columns,
        'table_data': table_data
    }
    
    dados_por_tipo['Histórico'] = grid_context

    return render(request, 'proventos/historico_portfolio.html', {
        'dados_por_tipo': dados_por_tipo
    })

@login_required
def atualizar_historico_view(request):
    if request.method == 'POST':
        gerar_historico_portfolio()
    return redirect('proventos:historico')

    
=======
from django.views.generic import ListView
from django.db import connection
import pandas as pd
from Atualizar_Transacoes.services.gerar_portfolios import calcular_posicao_portfolio
from .services.coletar_proventos import atualizar_proventos
from django.contrib import messages
from django.shortcuts import render
from .models import Provento

class ProventosListView(ListView):
    model = Provento
    template_name = 'proventos/proventos.html'
    context_object_name = 'proventos'
    ordering = ['-data_com']

def atualizar_dados_proventos(request):
    atualizar_proventos()
    messages.success(request, 'Proventos atualizados com sucesso!')
    return redirect('proventos:lista')
>>>>>>> 18c34b6243b7ecca8b79329a6c5b8cc51857778c
