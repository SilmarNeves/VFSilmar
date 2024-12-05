from django.urls import path
from . import views

app_name = 'Atualizar_Transacoes'

urlpatterns = [
    path('', views.index, name='index'),
    path('atualizar-sistema/', views.atualizar_sistema, name='atualizar_sistema'),
]
