# Generated by Django 3.1.1 on 2022-03-22 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modulo_configuracion', '0017_auto_20220322_0834'),
    ]

    operations = [
        migrations.AddField(
            model_name='clsordenescompramdl',
            name='delivery_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Fecha de entrega'),
        ),
    ]
