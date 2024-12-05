from django.urls import path
from . import views

urlpatterns = [
    path('', views.transacoes_view, name='transacoes'),
    path('export/', views.export_transactions, name='export_transactions'),
<<<<<<< HEAD
    path('atualizar-sistema/', views.atualizar_sistema_view, name='atualizar_sistema'),
=======
>>>>>>> 18c34b6243b7ecca8b79329a6c5b8cc51857778c
]