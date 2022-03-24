# Generated by Django 3.1.1 on 2022-03-22 08:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('modulo_configuracion', '0016_auto_20220317_0829'),
    ]

    operations = [
        migrations.RenameField(
            model_name='clscatalogoclientesmdl',
            old_name='credit_value',
            new_name='approved_amount',
        ),
        migrations.AlterField(
            model_name='clsasesorcomercialmdl',
            name='zone',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='modulo_configuracion.clszonaclientemdl', verbose_name='Zona'),
        ),
        migrations.AlterField(
            model_name='clscatalogoclientesmdl',
            name='customer_zone',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='modulo_configuracion.clszonaclientemdl'),
        ),
        migrations.AlterField(
            model_name='clscatalogoproductosmdl',
            name='product_subcat',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='modulo_configuracion.clssubcategoriaproductomdl', verbose_name='Subcategoría'),
        ),
    ]
