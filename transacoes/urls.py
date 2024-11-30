from django.urls import path
from . import views

urlpatterns = [
    path('', views.transacoes_view, name='transacoes'),
    path('export/', views.export_transactions, name='export_transactions'),
]