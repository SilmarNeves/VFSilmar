from django.db import models

class Movimentacao_Ativo(models.Model):
    papel = models.CharField(max_length=10)
    # Adicione outros campos necessários aqui
    
    class Meta:
        verbose_name = 'Movimentação de Ativo'
        verbose_name_plural = 'Movimentações de Ativos'
