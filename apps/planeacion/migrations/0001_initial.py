# Generated by Django 3.1.1 on 2022-03-17 18:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CommercialPlanning',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('update_date', models.DateTimeField(auto_now=True, null=True)),
                ('measurement_date', models.DateTimeField(auto_now_add=True)),
                ('monetary_goal', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Meta monetaria')),
                ('real', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Real')),
                ('fulfillment', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Cumplimiento')),
            ],
            options={
                'verbose_name': 'Planificación comercial',
                'verbose_name_plural': 'Planificaciones comerciales',
                'ordering': ['id'],
                'permissions': (('bia_adm_commercial_plan', 'Planificación comercial'),),
                'default_permissions': [],
            },
        ),
        migrations.CreateModel(
            name='CommercialPlanningAdvisor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('update_date', models.DateTimeField(auto_now=True, null=True)),
                ('monetary_goal', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Meta monetaria')),
                ('real', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Real')),
                ('fulfillment', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Cumplimiento')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CommercialPlanningCity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('update_date', models.DateTimeField(auto_now=True, null=True)),
                ('monetary_goal', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Meta monetaria')),
                ('real', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Real')),
                ('fulfillment', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Cumplimiento')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CommercialPlanningclsCategoriaClienteMdl',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('update_date', models.DateTimeField(auto_now=True, null=True)),
                ('monetary_goal', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Meta monetaria')),
                ('real', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Real')),
                ('fulfillment', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Cumplimiento')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CommercialPlanningCustomer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('update_date', models.DateTimeField(auto_now=True, null=True)),
                ('monetary_goal', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Meta monetaria')),
                ('real', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Real')),
                ('fulfillment', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Cumplimiento')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CommercialPlanningIndicators',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('update_date', models.DateTimeField(auto_now=True, null=True)),
                ('indicator_name', models.CharField(max_length=200, verbose_name='Nombre indicador')),
                ('monetary_goal', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Meta monetaria')),
                ('real', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Real')),
                ('fulfillment', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Cumplimiento')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CommercialPlanningZone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('update_date', models.DateTimeField(auto_now=True, null=True)),
                ('monetary_goal', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Meta monetaria')),
                ('real', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Real')),
                ('fulfillment', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Cumplimiento')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PromotionProducts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('update_date', models.DateTimeField(auto_now=True, null=True)),
                ('quantity', models.PositiveIntegerField(verbose_name='Cantidad')),
                ('unit_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='Precio unitario')),
                ('dcto', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Descuento')),
                ('prom_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='Precio descuento')),
            ],
            options={
                'verbose_name': 'Promoción producto',
                'verbose_name_plural': 'Promociones productos',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Promotions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('update_date', models.DateTimeField(auto_now=True, null=True)),
                ('name', models.CharField(max_length=50, verbose_name='Nombre promoción')),
                ('desc', models.TextField(verbose_name='Descripción promoción')),
                ('quantity', models.PositiveIntegerField(verbose_name='Cantidad disponible')),
                ('cons', models.TextField(blank=True, null=True, verbose_name='Consideraciones')),
                ('obs', models.TextField(blank=True, null=True, verbose_name='Observaciones')),
                ('expiration_date', models.DateField(default=datetime.datetime.now, verbose_name='Fecha de vigencia')),
            ],
            options={
                'verbose_name': 'Promoción',
                'verbose_name_plural': 'Promociones',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='PurchasePlanning',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('update_date', models.DateTimeField(auto_now=True, null=True)),
                ('measurement_date', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de medición')),
                ('monetary_goal', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Meta monetaria')),
                ('real', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Real')),
                ('fulfillment', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Cumplimiento')),
            ],
            options={
                'verbose_name': 'Planificación compras',
                'verbose_name_plural': 'Planificaciones compras',
                'ordering': ['id'],
                'permissions': (('bia_adm_purchase_plan', 'Planificación compras'),),
                'default_permissions': [],
            },
        ),
        migrations.CreateModel(
            name='WarehousePlanning',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('update_date', models.DateTimeField(auto_now=True, null=True)),
                ('measurement_date', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de medición')),
                ('monetary_goal', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Meta monetaria')),
                ('real', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Real')),
                ('fulfillment', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Cumplimiento')),
            ],
            options={
                'verbose_name': 'Planificación compras',
                'verbose_name_plural': 'Planificaciones compras',
                'ordering': ['id'],
                'permissions': (('bia_adm_warehouse_plan', 'Planificación almacén'),),
                'default_permissions': [],
            },
        ),
    ]
