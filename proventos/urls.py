from django.urls import path
from . import views

app_name = 'proventos'

urlpatterns = [
    path('historico/', views.historico_portfolio_view, name='historico'),
]
