from django.shortcuts import render
from django.http import HttpResponse
from .services.atualizar_transacoes import atualizar_transacoes
from .services.gerar_portfolios import gerar_portfolios
from cotacoes.utils import atualizar_cotacao_otimizado
from .services.atualizar_sistema import atualizar_sistema
from django.http import JsonResponse



def index(request):
    return render(request, 'atualizar_transacoes/index.html')

def atualizar_sistema(request):
    try:
        atualizar_sistema()
        return JsonResponse({'status': 'success', 'message': 'Sistema atualizado com sucesso!'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

def atualizar_sistema(request):
    atualizar_transacoes()
    gerar_portfolios()
    atualizar_cotacao_otimizado()
    atualizar_proventos()  # Nova função
    return HttpResponse("Sistema atualizado com sucesso!")
