# Generated by Django 3.1.1 on 2022-02-23 11:43

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('modulo_configuracion', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerDebt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('update_date', models.DateTimeField(auto_now=True, null=True)),
                ('order_value', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Valor orden')),
                ('term', models.PositiveSmallIntegerField(default=0, verbose_name='Cuotas')),
                ('next_payment_date', models.DateField(default=datetime.datetime.now, verbose_name='Fecha de próximo pago pedido')),
                ('next_payment_value', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Valor próximo pago pedido')),
                ('balance_payment', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Saldo pendiente de pago')),
                ('credit_value', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Valor crédito')),
                ('balance_credit_value', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Saldo crédito')),
                ('state', models.CharField(blank=True, choices=[('AC', 'Activa'), ('CE', 'Cerrada'), ('VE', 'Vencida')], default='AC', max_length=200, null=True, verbose_name='Estado')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_configuracion.clscatalogoclientesmdl')),
            ],
            options={
                'verbose_name': 'Cartera cliente',
                'verbose_name_plural': 'Cartera clientes',
                'ordering': ['id'],
                'permissions': (('bia_com_cust_debt', 'Cartera clientes'),),
                'default_permissions': [],
            },
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('update_date', models.DateTimeField(auto_now=True, null=True)),
                ('doc_number', models.CharField(blank=True, max_length=200, null=True, verbose_name='Documento Nº')),
                ('order_date', models.DateField(default=datetime.datetime.now, verbose_name='Fecha de pedido')),
                ('payment_method', models.CharField(choices=[('CR', 'Crédito'), ('CO', 'Contado')], default='CO', max_length=200, verbose_name='Método de pago')),
                ('delivery_date', models.DateField(default=datetime.datetime.now, verbose_name='Fecha de entrega')),
                ('delivery_address', models.CharField(max_length=200, verbose_name='Dirección de entrega')),
                ('subtotal', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='Subtotal')),
                ('iva', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Iva')),
                ('discount', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Descuento')),
                ('total', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='Total')),
                ('observations', models.TextField(blank=True, null=True, verbose_name='Observaciones')),
                ('state', models.CharField(choices=[('AB', 'Abierta'), ('CU', 'Cumplida'), ('CE', 'Cerrada')], default='AB', max_length=200, verbose_name='Estado')),
                ('identification', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_configuracion.clscatalogoclientesmdl')),
                ('user_creation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modulo_comercial_orders_creation', to=settings.AUTH_USER_MODEL)),
                ('user_update', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modulo_comercial_orders_updated', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Pedido cliente',
                'verbose_name_plural': 'Pedidos clientes',
                'ordering': ['id'],
                'permissions': (('bia_com_order', 'Pedidos'),),
                'default_permissions': [],
            },
        ),
        migrations.CreateModel(
            name='Quotes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('update_date', models.DateTimeField(auto_now=True, null=True)),
                ('quote_date', models.DateField(default=datetime.datetime.now, verbose_name='Fecha de cotización')),
                ('subtotal', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='Subtotal')),
                ('iva', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Iva')),
                ('discount', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Descuento')),
                ('total', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='Total')),
                ('observations', models.TextField(blank=True, null=True, verbose_name='Observaciones')),
                ('identification', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_configuracion.clscatalogoclientesmdl')),
                ('user_creation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modulo_comercial_quotes_creation', to=settings.AUTH_USER_MODEL)),
                ('user_update', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modulo_comercial_quotes_updated', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Cotización cliente',
                'verbose_name_plural': 'Cotizaciones clientes',
                'ordering': ['id'],
                'permissions': (('bia_com_quote', 'Cotizaciones'),),
                'default_permissions': [],
            },
        ),
        migrations.CreateModel(
            name='VisitsRoute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('update_date', models.DateTimeField(auto_now=True, null=True)),
                ('visit_date', models.DateField(default=datetime.datetime.now, verbose_name='Fecha de visita')),
                ('start_time', models.CharField(max_length=200, verbose_name='Hora inicio visita')),
                ('end_time', models.CharField(max_length=200, verbose_name='Hora fin visita')),
                ('visit_time', models.CharField(max_length=200, verbose_name='Tiempo de visita')),
                ('observations', models.TextField(verbose_name='Observaciones visita')),
                ('state', models.CharField(choices=[('AC', 'Activo'), ('IN', 'Inactivo')], default='AC', max_length=200, verbose_name='Estado')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_configuracion.clscatalogoclientesmdl', verbose_name='Cliente')),
                ('user_creation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modulo_comercial_visitsroute_creation', to=settings.AUTH_USER_MODEL)),
                ('user_update', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modulo_comercial_visitsroute_updated', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Ruta de visita',
                'verbose_name_plural': 'Ruta de visitas',
                'ordering': ['id'],
                'default_permissions': [],
            },
        ),
        migrations.CreateModel(
            name='ScheduleCall',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('update_date', models.DateTimeField(auto_now=True, null=True)),
                ('call_date', models.DateField(default=datetime.datetime.now, verbose_name='Fecha de llamada')),
                ('start_call', models.DateTimeField(verbose_name='Hora inicio llamada')),
                ('end_call', models.DateTimeField(verbose_name='Hora fin llamada')),
                ('call_time', models.DurationField(verbose_name='Tiempo de llamada')),
                ('obs', models.TextField(verbose_name='Observaciones')),
                ('state', models.CharField(choices=[('AC', 'Activo'), ('IN', 'Inactivo')], default='AC', max_length=200, verbose_name='Estado')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_configuracion.clscatalogoclientesmdl')),
                ('user_creation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modulo_comercial_schedulecall_creation', to=settings.AUTH_USER_MODEL)),
                ('user_update', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modulo_comercial_schedulecall_updated', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Agenda llamada',
                'verbose_name_plural': 'Agenda llamadas',
                'ordering': ['id'],
                'permissions': (('bia_com_sch_call', 'Agenda de llamadas'),),
                'default_permissions': [],
            },
        ),
        migrations.CreateModel(
            name='QuotesDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('update_date', models.DateTimeField(auto_now=True, null=True)),
                ('quantity', models.PositiveSmallIntegerField(default=0, verbose_name='Cantidad')),
                ('lead_time', models.PositiveSmallIntegerField(default=0, verbose_name='Tiempo de entrega')),
                ('unit_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='Precio unitario')),
                ('subtotal', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='Subtotal')),
                ('iva', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Iva')),
                ('discount', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Descuento')),
                ('total', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='Total')),
                ('due_date', models.DateField(default=datetime.datetime.now, verbose_name='Fecha de vigencia')),
                ('product_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_configuracion.clscatalogoproductosmdl', verbose_name='Producto')),
                ('quote', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_comercial.quotes', verbose_name='Cotización')),
                ('user_creation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modulo_comercial_quotesdetail_creation', to=settings.AUTH_USER_MODEL)),
                ('user_update', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modulo_comercial_quotesdetail_updated', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Detalle cotización',
                'verbose_name_plural': 'Detalle cotizaciones',
                'ordering': ['id'],
                'default_permissions': [],
            },
        ),
        migrations.CreateModel(
            name='OrdersDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('update_date', models.DateTimeField(auto_now=True, null=True)),
                ('quantity', models.PositiveSmallIntegerField(default=0, verbose_name='Cantidad')),
                ('unit_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='Precio unitario')),
                ('subtotal', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='Subtotal')),
                ('iva', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Iva')),
                ('discount', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='Descuento')),
                ('total', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='Total')),
                ('state', models.CharField(choices=[('AB', 'Abierta'), ('CU', 'Cumplida'), ('CE', 'Cerrada')], default='AB', max_length=200, verbose_name='Estado')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_comercial.orders', verbose_name='Pedido')),
                ('product_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_configuracion.clscatalogoproductosmdl', verbose_name='Producto')),
                ('user_creation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modulo_comercial_ordersdetail_creation', to=settings.AUTH_USER_MODEL)),
                ('user_update', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modulo_comercial_ordersdetail_updated', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Detalle pedido',
                'verbose_name_plural': 'Detalle pedidos',
                'ordering': ['id'],
                'default_permissions': [],
            },
        ),
        migrations.CreateModel(
            name='LostSales',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('update_date', models.DateTimeField(auto_now=True, null=True)),
                ('order_date', models.DateField(verbose_name='Fecha de venta')),
                ('quantity', models.PositiveSmallIntegerField(verbose_name='Cantidad')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_configuracion.clscatalogoclientesmdl')),
                ('product_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_configuracion.clscatalogoproductosmdl', verbose_name='Producto')),
                ('user_creation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modulo_comercial_lostsales_creation', to=settings.AUTH_USER_MODEL)),
                ('user_update', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modulo_comercial_lostsales_updated', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Venta perdida',
                'verbose_name_plural': 'Ventas perdidas',
                'ordering': ['id'],
                'default_permissions': [],
            },
        ),
        migrations.CreateModel(
            name='CustomerPayments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('update_date', models.DateTimeField(auto_now=True, null=True)),
                ('payment', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='Pago')),
                ('obs', models.TextField(verbose_name='Observaciones')),
                ('cartera', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_comercial.customerdebt', verbose_name='Cartera')),
                ('user_creation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modulo_comercial_customerpayments_creation', to=settings.AUTH_USER_MODEL)),
                ('user_update', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modulo_comercial_customerpayments_updated', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Pago cliente',
                'verbose_name_plural': 'Pagos clientes',
                'ordering': ['id'],
                'permissions': (('bia_com_cust_pay', 'Pagos clientes'),),
                'default_permissions': [],
            },
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
