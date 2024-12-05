from django.urls import path
from . import views

app_name = 'proventos'

urlpatterns = [
<<<<<<< HEAD
    path('historico/', views.historico_portfolio_view, name='historico'),
=======
    path('', views.ProventosListView.as_view(), name='lista'),
    path('atualizar/', views.atualizar_dados_proventos, name='atualizar'),
>>>>>>> 18c34b6243b7ecca8b79329a6c5b8cc51857778c
]
