from django.db import models
<<<<<<< HEAD

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
=======
from datetime import datetime

class Provento(models.Model):
    class Meta:
        db_table = 'proventos'
        managed = False
    
    papel = models.CharField(max_length=10, primary_key=True)
    data_com = models.DateField()
    data_pagamento = models.DateField()
    tipo_provento = models.CharField(max_length=50)
    valor_provento = models.DecimalField(max_digits=10, decimal_places=4)
    por_quantas_acoes = models.IntegerField()

    def get_data_com_formatted(self):
        return self.data_com.strftime("%d/%m/%Y") if self.data_com else ''

    def get_data_pagamento_formatted(self):
        return self.data_pagamento.strftime("%d/%m/%Y") if self.data_pagamento else ''
>>>>>>> 18c34b6243b7ecca8b79329a6c5b8cc51857778c
