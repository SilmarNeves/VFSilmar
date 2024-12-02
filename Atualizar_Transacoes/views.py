from django.shortcuts import render
from django.http import HttpResponse
from .services.atualizar_transacoes import atualizar_transacoes
from .services.gerar_portfolios import gerar_portfolios
from cotacoes.utils import atualizar_cotacao_otimizado
from proventos.services.coletar_proventos import atualizar_proventos

def index(request):
    return render(request, 'atualizar_transacoes/index.html')

def atualizar_sistema(request):
    atualizar_transacoes()
    gerar_portfolios()
    atualizar_cotacao_otimizado()
    atualizar_proventos()  # Nova função
    return HttpResponse("Sistema atualizado com sucesso!")
