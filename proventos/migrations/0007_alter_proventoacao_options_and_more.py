# Generated by Django 5.1.3 on 2024-12-06 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proventos', '0006_auto_20241206_1213'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='proventoacao',
            options={'ordering': ['-data_com', 'ativo']},
        ),
        migrations.RenameField(
            model_name='proventoacao',
            old_name='papel',
            new_name='ativo',
        ),
        migrations.RemoveField(
            model_name='proventoacao',
            name='quantidade_acoes',
        ),
        migrations.RemoveField(
            model_name='proventoacao',
            name='valor',
        ),
        migrations.AddField(
            model_name='proventoacao',
            name='por_quantas_acoes',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='proventoacao',
            name='valor_provento',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='proventoacao',
            name='data_pagamento',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='proventoacao',
            name='tipo_provento',
            field=models.CharField(max_length=20),
        ),
    ]
