from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .services.gerar_historico_portfolio import gerar_historico_portfolio
from .models import HistoricoPortfolio, ProventoAcao
from .services.coletores import coletar_proventos

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

from django.shortcuts import render
from .models import ProventoAcao

def lista_proventos(request):
    proventos = ProventoAcao.objects.all().order_by('-data_com')
    return render(request, 'proventos/lista.html', {'proventos': proventos})

def atualizar_proventos(request):
    if request.method == 'POST':
        papeis = ["MGLU3", "PETR4", "ASAI3", "HAPV3", "VIIA3"]
        coletar_proventos(papeis)
        return redirect('proventos:lista_proventos')
    return render(request, 'proventos/atualizar.html')
