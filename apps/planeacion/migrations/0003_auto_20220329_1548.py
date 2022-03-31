# Generated by Django 3.1.1 on 2022-03-29 15:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('planeacion', '0002_auto_20220317_1814'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='commercialplanningadvisor',
            name='commercial_advisor',
        ),
        migrations.RemoveField(
            model_name='commercialplanningadvisor',
            name='planning',
        ),
        migrations.RemoveField(
            model_name='commercialplanningadvisor',
            name='user_creation',
        ),
        migrations.RemoveField(
            model_name='commercialplanningadvisor',
            name='user_update',
        ),
        migrations.RemoveField(
            model_name='commercialplanningcity',
            name='city',
        ),
        migrations.RemoveField(
            model_name='commercialplanningcity',
            name='planning',
        ),
        migrations.RemoveField(
            model_name='commercialplanningcity',
            name='user_creation',
        ),
        migrations.RemoveField(
            model_name='commercialplanningcity',
            name='user_update',
        ),
        migrations.RemoveField(
            model_name='commercialplanningclscategoriaclientemdl',
            name='customer_cat',
        ),
        migrations.RemoveField(
            model_name='commercialplanningclscategoriaclientemdl',
            name='planning',
        ),
        migrations.RemoveField(
            model_name='commercialplanningclscategoriaclientemdl',
            name='user_creation',
        ),
        migrations.RemoveField(
            model_name='commercialplanningclscategoriaclientemdl',
            name='user_update',
        ),
        migrations.RemoveField(
            model_name='commercialplanningcustomer',
            name='customer',
        ),
        migrations.RemoveField(
            model_name='commercialplanningcustomer',
            name='planning',
        ),
        migrations.RemoveField(
            model_name='commercialplanningcustomer',
            name='user_creation',
        ),
        migrations.RemoveField(
            model_name='commercialplanningcustomer',
            name='user_update',
        ),
        migrations.RemoveField(
            model_name='commercialplanningindicators',
            name='planning',
        ),
        migrations.RemoveField(
            model_name='commercialplanningindicators',
            name='user_creation',
        ),
        migrations.RemoveField(
            model_name='commercialplanningindicators',
            name='user_update',
        ),
        migrations.RemoveField(
            model_name='commercialplanningzone',
            name='customer_zone',
        ),
        migrations.RemoveField(
            model_name='commercialplanningzone',
            name='planning',
        ),
        migrations.RemoveField(
            model_name='commercialplanningzone',
            name='user_creation',
        ),
        migrations.RemoveField(
            model_name='commercialplanningzone',
            name='user_update',
        ),
        migrations.RemoveField(
            model_name='promotionproducts',
            name='product',
        ),
        migrations.RemoveField(
            model_name='promotionproducts',
            name='prom',
        ),
        migrations.RemoveField(
            model_name='promotionproducts',
            name='sales_unit',
        ),
        migrations.RemoveField(
            model_name='promotionproducts',
            name='user_creation',
        ),
        migrations.RemoveField(
            model_name='promotionproducts',
            name='user_update',
        ),
        migrations.RemoveField(
            model_name='promotions',
            name='user_creation',
        ),
        migrations.RemoveField(
            model_name='promotions',
            name='user_update',
        ),
        migrations.RemoveField(
            model_name='purchaseplanning',
            name='user_creation',
        ),
        migrations.RemoveField(
            model_name='purchaseplanning',
            name='user_update',
        ),
        migrations.RemoveField(
            model_name='warehouseplanning',
            name='user_creation',
        ),
        migrations.RemoveField(
            model_name='warehouseplanning',
            name='user_update',
        ),
        migrations.DeleteModel(
            name='CommercialPlanning',
        ),
        migrations.DeleteModel(
            name='CommercialPlanningAdvisor',
        ),
        migrations.DeleteModel(
            name='CommercialPlanningCity',
        ),
        migrations.DeleteModel(
            name='CommercialPlanningclsCategoriaClienteMdl',
        ),
        migrations.DeleteModel(
            name='CommercialPlanningCustomer',
        ),
        migrations.DeleteModel(
            name='CommercialPlanningIndicators',
        ),
        migrations.DeleteModel(
            name='CommercialPlanningZone',
        ),
        migrations.DeleteModel(
            name='PromotionProducts',
        ),
        migrations.DeleteModel(
            name='Promotions',
        ),
        migrations.DeleteModel(
            name='PurchasePlanning',
        ),
        migrations.DeleteModel(
            name='WarehousePlanning',
        ),
    ]