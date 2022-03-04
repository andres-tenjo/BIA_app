# Generated by Django 3.1.1 on 2022-02-24 15:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('modulo_compras', '0001_initial'),
        ('modulo_configuracion', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='supplierspayments',
            name='user_creation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modulo_compras_supplierspayments_creation', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='supplierspayments',
            name='user_update',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modulo_compras_supplierspayments_updated', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='supplierquotedetail',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_configuracion.clscatalogoproductosmdl', verbose_name='Producto'),
        ),
        migrations.AddField(
            model_name='supplierquotedetail',
            name='supplier_quote',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_compras.supplierquote', verbose_name='Cotización'),
        ),
        migrations.AddField(
            model_name='supplierquotedetail',
            name='user_creation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modulo_compras_supplierquotedetail_creation', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='supplierquotedetail',
            name='user_update',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modulo_compras_supplierquotedetail_updated', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='supplierquote',
            name='identification',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_configuracion.clscatalogoproveedoresmdl', verbose_name='Proveedor'),
        ),
        migrations.AddField(
            model_name='supplierquote',
            name='user_creation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modulo_compras_supplierquote_creation', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='supplierquote',
            name='user_update',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modulo_compras_supplierquote_updated', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='supplierdebt',
            name='order_purchase',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_compras.orderpurchase', verbose_name='Orden de compra'),
        ),
        migrations.AddField(
            model_name='supplierdebt',
            name='supplier',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_configuracion.clscatalogoproveedoresmdl', verbose_name='Proveedor'),
        ),
        migrations.AddField(
            model_name='supplierdebt',
            name='user_creation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modulo_compras_supplierdebt_creation', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='supplierdebt',
            name='user_update',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modulo_compras_supplierdebt_updated', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='orderpurchasedetail',
            name='order_purchase',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_compras.orderpurchase', verbose_name='Orden de compra'),
        ),
        migrations.AddField(
            model_name='orderpurchasedetail',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_configuracion.clscatalogoproductosmdl'),
        ),
        migrations.AddField(
            model_name='orderpurchasedetail',
            name='user_creation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modulo_compras_orderpurchasedetail_creation', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='orderpurchasedetail',
            name='user_update',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modulo_compras_orderpurchasedetail_updated', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='orderpurchase',
            name='identification',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_configuracion.clscatalogoproveedoresmdl', verbose_name='Proveedor'),
        ),
        migrations.AddField(
            model_name='orderpurchase',
            name='user_creation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modulo_compras_orderpurchase_creation', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='orderpurchase',
            name='user_update',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modulo_compras_orderpurchase_updated', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='evaluationsuppliers',
            name='supplier',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_configuracion.clscatalogoproveedoresmdl', verbose_name='Proveedor'),
        ),
        migrations.AddField(
            model_name='evaluationsuppliers',
            name='user_creation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modulo_compras_evaluationsuppliers_creation', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='evaluationsuppliers',
            name='user_update',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modulo_compras_evaluationsuppliers_updated', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='entregasincumplidas',
            name='order_purchase',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_compras.orderpurchase', verbose_name='Orden de compra'),
        ),
        migrations.AddField(
            model_name='entregasincumplidas',
            name='supplier',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_configuracion.clscatalogoproveedoresmdl', verbose_name='Proveedor'),
        ),
        migrations.AddField(
            model_name='entregasincumplidas',
            name='user_creation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modulo_compras_entregasincumplidas_creation', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='entregasincumplidas',
            name='user_update',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modulo_compras_entregasincumplidas_updated', to=settings.AUTH_USER_MODEL),
        ),
    ]
