from django.shortcuts import render, redirect
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
    template_name = 'proventos/lista.html'
    context_object_name = 'proventos'
    ordering = ['-data_com']

def atualizar_dados_proventos(request):
    atualizar_proventos()
    messages.success(request, 'Proventos atualizados com sucesso!')
    return redirect('proventos:lista')
