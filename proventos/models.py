from django.db import models
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
