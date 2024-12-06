from django.urls import path
from . import views

app_name = 'proventos'

urlpatterns = [
    path('historico/', views.historico_portfolio_view, name='historico'),
    path('lista/', views.lista_proventos, name='lista_proventos'),
    path('atualizar/', views.atualizar_proventos, name='atualizar_proventos'),
]
