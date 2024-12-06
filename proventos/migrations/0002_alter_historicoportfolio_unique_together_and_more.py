# Generated by Django 5.1.3 on 2024-12-04 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proventos', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='historicoportfolio',
            unique_together=set(),
        ),
        migrations.AddField(
            model_name='historicoportfolio',
            name='carteira',
            field=models.CharField(default='Consolidada', max_length=20),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='historicoportfolio',
            unique_together={('data', 'ativo', 'carteira')},
        ),
    ]
