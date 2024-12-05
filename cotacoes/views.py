from django.shortcuts import render, redirect
from .utils import atualizar_cotacao_otimizado
from django.contrib import messages

from django.shortcuts import render, redirect
from .utils import atualizar_cotacao_otimizado, get_ultimo_dia_util, get_dia_util_anterior
from django.contrib import messages
from django.utils import timezone
import pytz
import logging
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

logger = logging.getLogger(__name__)

@login_required
def atualizar_cotacao_view(request):
    if request.method == 'POST':
        try:
            # Obtém as datas
            ultimo_dia_util = get_ultimo_dia_util()
            dia_anterior = get_dia_util_anterior(ultimo_dia_util)
            
            logger.info(f"\nBuscando cotações:")
            logger.info(f"Último dia útil: {ultimo_dia_util} ({ultimo_dia_util.strftime('%A')})")
            logger.info(f"Dia útil anterior: {dia_anterior} ({dia_anterior.strftime('%A')})")
            
            # Executa a atualização com log detalhado
            resultado = atualizar_cotacao_otimizado(debug=True)
            
            # Registra o horário da atualização
            tz = pytz.timezone('America/Sao_Paulo')
            hora_atual = timezone.now().astimezone(tz).strftime('%H:%M:%S')
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': f'Cotações atualizadas com sucesso! Hora: {hora_atual}',
                    'debug_info': resultado
                })
            
            messages.success(request, f'Cotações atualizadas com sucesso! Hora: {hora_atual}')
            next_url = request.POST.get('next', 'carteira')
            return redirect(next_url)
            
        except Exception as e:
            logger.error(f"Erro na atualização: {str(e)}")
            messages.error(request, f'Erro ao atualizar cotações: {str(e)}')
            return redirect('carteira')
    
    ultima_atualizacao = timezone.now()
    return render(request, 'carteira/carteira.html', {'ultima_atualizacao': ultima_atualizacao})

# transacoes/views.py
@login_required
def atualizar_tudo(request):
    session = HTMLSession()
    
    
    # Acessar página de atualização de cotações
    response = session.get('http://127.0.0.1:8000/atualizacao/atualizar-cotacao/')
    if response.status_code != 200:
        return JsonResponse({"success": False, "message": "Erro ao acessar página de atualização de cotações"}, status=500)
    
    # Submeter o formulário para atualizar cotações
    form = response.html.find('form', first=True)
    if form:
        action_url = form.attrs.get('action')
        response = session.post(f'http://127.0.0.1:8000{action_url}', data={'csrfmiddlewaretoken': form.find('input[name="csrfmiddlewaretoken"]', first=True).attrs['value']})
        if response.status_code != 200:
            return JsonResponse({"success": False, "message": "Erro ao atualizar cotações"}, status=500)
    else:
        return JsonResponse({"success": False, "message": "Formulário de atualização de cotações não encontrado"}, status=500)
    
    return JsonResponse({"success": True, "message": "Atualização completa com sucesso!"})
