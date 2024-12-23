# Generated by Django 5.1.3 on 2024-11-16 18:25

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financeiro', '0003_alter_transacao_data_alter_transacao_tipo'),
    ]

    operations = [
        migrations.CreateModel(
            name='SaldosFaturas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateField(default=django.utils.timezone.now)),
                ('saldo_bradesco', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('saldo_itau', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('saldo_inter', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('fatura_bradesco', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('fatura_itau', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('fatura_inter', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
            ],
        ),
    ]
