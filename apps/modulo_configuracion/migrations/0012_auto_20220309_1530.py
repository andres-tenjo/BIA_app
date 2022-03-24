# Generated by Django 3.1.1 on 2022-03-09 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modulo_configuracion', '0011_auto_20220309_1018'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clsdetalleordenescompramdl',
            name='iva',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='IVA'),
        ),
        migrations.AlterField(
            model_name='clsdetallepedidosmdl',
            name='iva',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='IVA'),
        ),
        migrations.AlterField(
            model_name='clsordenescompramdl',
            name='iva',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='IVA'),
        ),
        migrations.AlterField(
            model_name='clspedidosmdl',
            name='iva',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='IVA'),
        ),
    ]