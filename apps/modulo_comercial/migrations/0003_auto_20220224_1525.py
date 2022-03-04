# Generated by Django 3.1.1 on 2022-02-24 15:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('modulo_comercial', '0002_visitsroute_customer'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('modulo_configuracion', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='visitsroute',
            name='user_creation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modulo_comercial_visitsroute_creation', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='visitsroute',
            name='user_update',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modulo_comercial_visitsroute_updated', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='schedulecall',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_configuracion.clscatalogoclientesmdl'),
        ),
        migrations.AddField(
            model_name='schedulecall',
            name='user_creation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modulo_comercial_schedulecall_creation', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='schedulecall',
            name='user_update',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modulo_comercial_schedulecall_updated', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='quotesdetail',
            name='product_code',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_configuracion.clscatalogoproductosmdl', verbose_name='Producto'),
        ),
        migrations.AddField(
            model_name='quotesdetail',
            name='quote',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_comercial.quotes', verbose_name='Cotización'),
        ),
        migrations.AddField(
            model_name='quotesdetail',
            name='user_creation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modulo_comercial_quotesdetail_creation', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='quotesdetail',
            name='user_update',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modulo_comercial_quotesdetail_updated', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='quotes',
            name='identification',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_configuracion.clscatalogoclientesmdl'),
        ),
        migrations.AddField(
            model_name='quotes',
            name='user_creation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modulo_comercial_quotes_creation', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='quotes',
            name='user_update',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modulo_comercial_quotes_updated', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='ordersdetail',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_comercial.orders', verbose_name='Pedido'),
        ),
        migrations.AddField(
            model_name='ordersdetail',
            name='product_code',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_configuracion.clscatalogoproductosmdl', verbose_name='Producto'),
        ),
        migrations.AddField(
            model_name='ordersdetail',
            name='user_creation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modulo_comercial_ordersdetail_creation', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='ordersdetail',
            name='user_update',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modulo_comercial_ordersdetail_updated', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='orders',
            name='identification',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_configuracion.clscatalogoclientesmdl'),
        ),
        migrations.AddField(
            model_name='orders',
            name='user_creation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modulo_comercial_orders_creation', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='orders',
            name='user_update',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modulo_comercial_orders_updated', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='lostsales',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_configuracion.clscatalogoclientesmdl'),
        ),
        migrations.AddField(
            model_name='lostsales',
            name='product_code',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_configuracion.clscatalogoproductosmdl', verbose_name='Producto'),
        ),
        migrations.AddField(
            model_name='lostsales',
            name='user_creation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modulo_comercial_lostsales_creation', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='lostsales',
            name='user_update',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modulo_comercial_lostsales_updated', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='customerpayments',
            name='cartera',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_comercial.customerdebt', verbose_name='Cartera'),
        ),
        migrations.AddField(
            model_name='customerpayments',
            name='user_creation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modulo_comercial_customerpayments_creation', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='customerpayments',
            name='user_update',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modulo_comercial_customerpayments_updated', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='customerdebt',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_configuracion.clscatalogoclientesmdl'),
        ),
        migrations.AddField(
            model_name='customerdebt',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_comercial.orders', verbose_name='Pedido'),
        ),
        migrations.AddField(
            model_name='customerdebt',
            name='user_creation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modulo_comercial_customerdebt_creation', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='customerdebt',
            name='user_update',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modulo_comercial_customerdebt_updated', to=settings.AUTH_USER_MODEL),
        ),
    ]
