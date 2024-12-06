from django.db import models

class HistoricoPortfolio(models.Model):
    data = models.DateField()
    ativo = models.CharField(max_length=10)
    quantidade = models.IntegerField()
    preco_medio = models.DecimalField(max_digits=10, decimal_places=2)
    tipo = models.CharField(max_length=10)  # Ação ou FII
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)
    carteira = models.CharField(max_length=20)  # Consolidada, Silmar ou Monica

    class Meta:
        unique_together = ['data', 'ativo', 'carteira']
        indexes = [
            models.Index(fields=['data']),
            models.Index(fields=['ativo'])
        ]

class ProventoAcao(models.Model):
    papel = models.CharField(max_length=10)
    data_com = models.DateField()
    data_pagamento = models.DateField(null=True, blank=True)
    tipo_provento = models.CharField(max_length=50)
    valor = models.DecimalField(max_digits=10, decimal_places=4)
    quantidade_acoes = models.IntegerField(default=1)

    class Meta:
        ordering = ['-data_com', 'papel']

