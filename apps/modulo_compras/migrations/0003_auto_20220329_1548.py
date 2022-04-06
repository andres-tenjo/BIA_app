# Generated by Django 3.1.1 on 2022-03-29 15:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('modulo_compras', '0002_auto_20220317_1814'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='evaluationsuppliers',
            name='supplier',
        ),
        migrations.RemoveField(
            model_name='evaluationsuppliers',
            name='user_creation',
        ),
        migrations.RemoveField(
            model_name='evaluationsuppliers',
            name='user_update',
        ),
        migrations.RemoveField(
            model_name='orderpurchase',
            name='identification',
        ),
        migrations.RemoveField(
            model_name='orderpurchase',
            name='user_creation',
        ),
        migrations.RemoveField(
            model_name='orderpurchase',
            name='user_update',
        ),
        migrations.RemoveField(
            model_name='orderpurchasedetail',
            name='order_purchase',
        ),
        migrations.RemoveField(
            model_name='orderpurchasedetail',
            name='product',
        ),
        migrations.RemoveField(
            model_name='orderpurchasedetail',
            name='user_creation',
        ),
        migrations.RemoveField(
            model_name='orderpurchasedetail',
            name='user_update',
        ),
        migrations.RemoveField(
            model_name='supplierdebt',
            name='order_purchase',
        ),
        migrations.RemoveField(
            model_name='supplierdebt',
            name='supplier',
        ),
        migrations.RemoveField(
            model_name='supplierdebt',
            name='user_creation',
        ),
        migrations.RemoveField(
            model_name='supplierdebt',
            name='user_update',
        ),
        migrations.RemoveField(
            model_name='supplierquote',
            name='identification',
        ),
        migrations.RemoveField(
            model_name='supplierquote',
            name='user_creation',
        ),
        migrations.RemoveField(
            model_name='supplierquote',
            name='user_update',
        ),
        migrations.RemoveField(
            model_name='supplierquotedetail',
            name='product',
        ),
        migrations.RemoveField(
            model_name='supplierquotedetail',
            name='supplier_quote',
        ),
        migrations.RemoveField(
            model_name='supplierquotedetail',
            name='user_creation',
        ),
        migrations.RemoveField(
            model_name='supplierquotedetail',
            name='user_update',
        ),
        migrations.RemoveField(
            model_name='supplierspayments',
            name='cartera',
        ),
        migrations.RemoveField(
            model_name='supplierspayments',
            name='user_creation',
        ),
        migrations.RemoveField(
            model_name='supplierspayments',
            name='user_update',
        ),
        migrations.DeleteModel(
            name='EntregasIncumplidas',
        ),
        migrations.DeleteModel(
            name='EvaluationSuppliers',
        ),
        migrations.DeleteModel(
            name='OrderPurchase',
        ),
        migrations.DeleteModel(
            name='OrderPurchaseDetail',
        ),
        migrations.DeleteModel(
            name='SupplierDebt',
        ),
        migrations.DeleteModel(
            name='SupplierQuote',
        ),
        migrations.DeleteModel(
            name='SupplierQuoteDetail',
        ),
        migrations.DeleteModel(
            name='SuppliersPayments',
        ),
    ]