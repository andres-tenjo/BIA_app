# Generated by Django 3.1.1 on 2022-03-17 18:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('modulo_configuracion', '0002_auto_20220317_1814'),
        ('modulo_logistica', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='warehouserevenuedetail',
            name='user_creation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modulo_logistica_warehouserevenuedetail_creation', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='warehouserevenuedetail',
            name='user_update',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modulo_logistica_warehouserevenuedetail_updated', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='warehouserevenuedetail',
            name='warehouse_entry',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_logistica.warehouserevenue', verbose_name='Entrada de almacén'),
        ),
        migrations.AddField(
            model_name='warehouserevenue',
            name='supplier',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_configuracion.clscatalogoproveedoresmdl', verbose_name='Proveedor'),
        ),
        migrations.AddField(
            model_name='warehouserevenue',
            name='user_creation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modulo_logistica_warehouserevenue_creation', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='warehouserevenue',
            name='user_update',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modulo_logistica_warehouserevenue_updated', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='warehouseoutflowsdetail',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_configuracion.clscatalogoproductosmdl'),
        ),
        migrations.AddField(
            model_name='warehouseoutflowsdetail',
            name='user_creation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modulo_logistica_warehouseoutflowsdetail_creation', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='warehouseoutflowsdetail',
            name='user_update',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modulo_logistica_warehouseoutflowsdetail_updated', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='warehouseoutflowsdetail',
            name='warehouse_exit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_logistica.warehouseoutflows', verbose_name='Salida'),
        ),
        migrations.AddField(
            model_name='warehouseoutflows',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_configuracion.clscatalogoclientesmdl', verbose_name='Cliente'),
        ),
        migrations.AddField(
            model_name='warehouseoutflows',
            name='user_creation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modulo_logistica_warehouseoutflows_creation', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='warehouseoutflows',
            name='user_update',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modulo_logistica_warehouseoutflows_updated', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='inventorycountdetail',
            name='inventory_count',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_logistica.inventorycount', verbose_name='Conteo de inventario'),
        ),
        migrations.AddField(
            model_name='inventorycountdetail',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_configuracion.clscatalogoproductosmdl'),
        ),
        migrations.AddField(
            model_name='inventorycountdetail',
            name='user_creation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modulo_logistica_inventorycountdetail_creation', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='inventorycountdetail',
            name='user_update',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modulo_logistica_inventorycountdetail_updated', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='inventorycount',
            name='user_creation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modulo_logistica_inventorycount_creation', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='inventorycount',
            name='user_update',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modulo_logistica_inventorycount_updated', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='inventory',
            name='inventory_count',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_logistica.inventorycount'),
        ),
        migrations.AddField(
            model_name='inventory',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_configuracion.clscatalogoproductosmdl'),
        ),
        migrations.AddField(
            model_name='inventory',
            name='user_creation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modulo_logistica_inventory_creation', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='inventory',
            name='user_update',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modulo_logistica_inventory_updated', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='inventory',
            name='warehouse_entry',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_logistica.warehouserevenue', verbose_name='Entrada'),
        ),
        migrations.AddField(
            model_name='inventory',
            name='warehouse_exit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_logistica.warehouseoutflows', verbose_name='Salida'),
        ),
    ]