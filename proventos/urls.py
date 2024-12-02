from django.urls import path
from . import views

app_name = 'proventos'

urlpatterns = [
    path('', views.ProventosListView.as_view(), name='lista'),
    path('atualizar/', views.atualizar_dados_proventos, name='atualizar'),
]
