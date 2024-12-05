from django.shortcuts import render
from django.http import HttpResponse
from .services.atualizar_transacoes import atualizar_transacoes
from .services.gerar_portfolios import gerar_portfolios
from cotacoes.utils import atualizar_cotacao_otimizado
<<<<<<< HEAD
from .services.atualizar_sistema import atualizar_sistema
from django.http import JsonResponse


=======
from proventos.services.coletar_proventos import atualizar_proventos
>>>>>>> 18c34b6243b7ecca8b79329a6c5b8cc51857778c

def index(request):
    return render(request, 'atualizar_transacoes/index.html')

def atualizar_sistema(request):
<<<<<<< HEAD
    try:
        atualizar_sistema()
        return JsonResponse({'status': 'success', 'message': 'Sistema atualizado com sucesso!'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

def atualizar_sistema(request):
=======
>>>>>>> 18c34b6243b7ecca8b79329a6c5b8cc51857778c
    atualizar_transacoes()
    gerar_portfolios()
    atualizar_cotacao_otimizado()
    atualizar_proventos()  # Nova função
    return HttpResponse("Sistema atualizado com sucesso!")
