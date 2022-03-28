# Generated by Django 3.1.1 on 2022-03-18 09:40

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
        migrations.AddField(
            model_name='clszonaclientemdl',
            name='user_creation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modulo_configuracion_clszonaclientemdl_creation', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='clszonaclientemdl',
            name='user_update',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modulo_configuracion_clszonaclientemdl_updated', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='clsunidadventamdl',
            name='user_creation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modulo_configuracion_clsunidadventamdl_creation', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='clsunidadventamdl',
            name='user_update',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modulo_configuracion_clsunidadventamdl_updated', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='clsunidadcompramdl',
            name='user_creation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modulo_configuracion_clsunidadcompramdl_creation', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='clsunidadcompramdl',
            name='user_update',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modulo_configuracion_clsunidadcompramdl_updated', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='clstrasladosbodegasmdl',
            name='user_creation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modulo_configuracion_clstrasladosbodegasmdl_creation', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='clstrasladosbodegasmdl',
            name='user_update',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modulo_configuracion_clstrasladosbodegasmdl_updated', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='clstbldetalleentradaalmacen',
            name='doc_number',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_configuracion.clsentradasalmacenmdl'),
        ),
        migrations.AddField(
            model_name='clstbldetalleentradaalmacen',
            name='product_code',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_configuracion.clscatalogoproductosmdl'),
        ),
        migrations.AddField(
            model_name='clssubcategoriaproductomdl',
            name='product_cat',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_configuracion.clscategoriaproductomdl', verbose_name='Categoría de producto'),
        ),
        migrations.AddField(
            model_name='clssubcategoriaproductomdl',
            name='user_creation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modulo_configuracion_clssubcategoriaproductomdl_creation', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='clssubcategoriaproductomdl',
            name='user_update',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modulo_configuracion_clssubcategoriaproductomdl_updated', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='clssalidasalmacenmdl',
            name='identification',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_configuracion.clscatalogoclientesmdl'),
        ),
        migrations.AddField(
            model_name='clssalidasalmacenmdl',
            name='store',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_configuracion.clscatalogobodegasmdl'),
        ),
        migrations.AddField(
            model_name='clssalidasalmacenmdl',
            name='user_creation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modulo_configuracion_clssalidasalmacenmdl_creation', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='clssalidasalmacenmdl',
            name='user_update',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modulo_configuracion_clssalidasalmacenmdl_updated', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='clssaldosinventariomdl',
            name='product_code',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_configuracion.clscatalogoproductosmdl'),
        ),
        migrations.AddField(
            model_name='clssaldosinventariomdl',
            name='store',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_configuracion.clscatalogobodegasmdl'),
        ),
        migrations.AddField(
            model_name='clsperfilempresamdl',
            name='city',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_configuracion.clsciudadesmdl'),
        ),
        migrations.AddField(
            model_name='clsperfilempresamdl',
            name='department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_configuracion.clsdepartamentosmdl'),
        ),
        migrations.AddField(
            model_name='clsperfilempresamdl',
            name='user_creation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modulo_configuracion_clsperfilempresamdl_creation', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='clsperfilempresamdl',
            name='user_update',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modulo_configuracion_clsperfilempresamdl_updated', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='clsobsequiosmdl',
            name='identification',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_configuracion.clscatalogoclientesmdl'),
        ),
        migrations.AddField(
            model_name='clsobsequiosmdl',
            name='store',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_configuracion.clscatalogobodegasmdl'),
        ),
        migrations.AddField(
            model_name='clsobsequiosmdl',
            name='user_creation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modulo_configuracion_clsobsequiosmdl_creation', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='clsobsequiosmdl',
            name='user_update',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modulo_configuracion_clsobsequiosmdl_updated', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='clsmargencategoriaclientemdl',
            name='customer_cat',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_configuracion.clscategoriaclientemdl'),
        ),
        migrations.AddField(
            model_name='clsmargencategoriaclientemdl',
            name='product_cat',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_configuracion.clscategoriaproductomdl'),
        ),
        migrations.AddField(
            model_name='clsmargencategoriaclientemdl',
            name='user_creation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modulo_configuracion_clsmargencategoriaclientemdl_creation', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='clsmargencategoriaclientemdl',
            name='user_update',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modulo_configuracion_clsmargencategoriaclientemdl_updated', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='clshistoricopedidosmdl',
            name='city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='modulo_configuracion.clsciudadesmdl'),
        ),
        migrations.AddField(
            model_name='clshistoricopedidosmdl',
            name='identification',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_configuracion.clscatalogoclientesmdl'),
        ),
        migrations.AddField(
            model_name='clshistoricopedidosmdl',
            name='product_code',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_configuracion.clscatalogoproductosmdl'),
        ),
        migrations.AddField(
            model_name='clshistoricopedidosmdl',
            name='store',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_configuracion.clscatalogobodegasmdl'),
        ),
        migrations.AddField(
            model_name='clshistoricoordenescompramdl',
            name='identification',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_configuracion.clscatalogoproveedoresmdl'),
        ),
        migrations.AddField(
            model_name='clshistoricoordenescompramdl',
            name='product_code',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_configuracion.clscatalogoproductosmdl'),
        ),
        migrations.AddField(
            model_name='clshistoricoordenescompramdl',
            name='store',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_configuracion.clscatalogobodegasmdl'),
        ),
        migrations.AddField(
            model_name='clshistoricomovimientosmdl',
            name='product_code',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_configuracion.clscatalogoproductosmdl'),
        ),
        migrations.AddField(
            model_name='clshistoricomovimientosmdl',
            name='store',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_configuracion.clscatalogobodegasmdl'),
        ),
        migrations.AddField(
            model_name='clshistoricomovimientosmdl',
            name='user_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='clshistoricomovimientosalternomdl',
            name='product_code',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_configuracion.clscatalogoproductosmdl'),
        ),
        migrations.AddField(
            model_name='clshistoricomovimientosalternomdl',
            name='store',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_configuracion.clscatalogobodegasmdl'),
        ),
        migrations.AddField(
            model_name='clshistoricomovimientosalternomdl',
            name='user_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='clsentradasalmacenmdl',
            name='identification',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_configuracion.clscatalogoproveedoresmdl'),
        ),
        migrations.AddField(
            model_name='clsentradasalmacenmdl',
            name='store',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_configuracion.clscatalogobodegasmdl'),
        ),
        migrations.AddField(
            model_name='clsentradasalmacenmdl',
            name='user_creation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modulo_configuracion_clsentradasalmacenmdl_creation', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='clsentradasalmacenmdl',
            name='user_update',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modulo_configuracion_clsentradasalmacenmdl_updated', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='clsdevolucionesproveedormdl',
            name='identification',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_configuracion.clscatalogoproveedoresmdl'),
        ),
        migrations.AddField(
            model_name='clsdevolucionesproveedormdl',
            name='store',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_configuracion.clscatalogobodegasmdl'),
        ),
        migrations.AddField(
            model_name='clsdevolucionesproveedormdl',
            name='user_creation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modulo_configuracion_clsdevolucionesproveedormdl_creation', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='clsdevolucionesproveedormdl',
            name='user_update',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modulo_configuracion_clsdevolucionesproveedormdl_updated', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='clsdevolucionesclientemdl',
            name='identification',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_configuracion.clscatalogoclientesmdl'),
        ),
        migrations.AddField(
            model_name='clsdevolucionesclientemdl',
            name='store',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_configuracion.clscatalogobodegasmdl'),
        ),
        migrations.AddField(
            model_name='clsdevolucionesclientemdl',
            name='user_creation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modulo_configuracion_clsdevolucionesclientemdl_creation', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='clsdevolucionesclientemdl',
            name='user_update',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modulo_configuracion_clsdevolucionesclientemdl_updated', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='clsdetalletrasladosbodegamdl',
            name='doc_number',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_configuracion.clstrasladosbodegasmdl'),
        ),
        migrations.AddField(
            model_name='clsdetalletrasladosbodegamdl',
            name='product_code',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_configuracion.clscatalogoproductosmdl'),
        ),
        migrations.AddField(
            model_name='clsdetalletrasladosbodegamdl',
            name='store',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='modulo_configuracion.clscatalogobodegasmdl'),
        ),
        migrations.AddField(
            model_name='clsdetallesalidasalmacenmdl',
            name='doc_number',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_configuracion.clssalidasalmacenmdl'),
        ),
        migrations.AddField(
            model_name='clsdetallesalidasalmacenmdl',
            name='product_code',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_configuracion.clscatalogoproductosmdl'),
        ),
        migrations.AddField(
            model_name='clsdetalleobsequiosmdl',
            name='doc_number',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_configuracion.clsobsequiosmdl'),
        ),
        migrations.AddField(
            model_name='clsdetalleobsequiosmdl',
            name='product_code',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_configuracion.clscatalogoproductosmdl'),
        ),
        migrations.AddField(
            model_name='clsdetalledevolucionesproveedormdl',
            name='doc_number',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_configuracion.clsdevolucionesproveedormdl'),
        ),
        migrations.AddField(
            model_name='clsdetalledevolucionesproveedormdl',
            name='product_code',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_configuracion.clscatalogoproductosmdl'),
        ),
        migrations.AddField(
            model_name='clsdetalledevolucionesclientemdl',
            name='doc_number',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_configuracion.clsdevolucionesclientemdl'),
        ),
        migrations.AddField(
            model_name='clsdetalledevolucionesclientemdl',
            name='product_code',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_configuracion.clscatalogoproductosmdl'),
        ),
        migrations.AddField(
            model_name='clsdetalleajusteinventariomdl',
            name='doc_number',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_configuracion.clsajusteinventariomdl'),
        ),
        migrations.AddField(
            model_name='clsdetalleajusteinventariomdl',
            name='product_code',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_configuracion.clscatalogoproductosmdl'),
        ),
        migrations.AddField(
            model_name='clsdetalleajusteinventariomdl',
            name='store',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_configuracion.clscatalogobodegasmdl'),
        ),
        migrations.AddField(
            model_name='clsdepartamentosmdl',
            name='user_creation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modulo_configuracion_clsdepartamentosmdl_creation', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='clsdepartamentosmdl',
            name='user_update',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modulo_configuracion_clsdepartamentosmdl_updated', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='clscondicionminimacompramdl',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_configuracion.clscatalogoproductosmdl'),
        ),
        migrations.AddField(
            model_name='clscondicionminimacompramdl',
            name='supplier',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_configuracion.clscatalogoproveedoresmdl'),
        ),
        migrations.AddField(
            model_name='clscondicionminimacompramdl',
            name='user_creation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modulo_configuracion_clscondicionminimacompramdl_creation', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='clscondicionminimacompramdl',
            name='user_update',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modulo_configuracion_clscondicionminimacompramdl_updated', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='clscondiciondescuentoproveedormdl',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_configuracion.clscatalogoproductosmdl'),
        ),
        migrations.AddField(
            model_name='clscondiciondescuentoproveedormdl',
            name='supplier',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_configuracion.clscatalogoproveedoresmdl'),
        ),
        migrations.AddField(
            model_name='clscondiciondescuentoproveedormdl',
            name='user_creation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modulo_configuracion_clscondiciondescuentoproveedormdl_creation', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='clscondiciondescuentoproveedormdl',
            name='user_update',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modulo_configuracion_clscondiciondescuentoproveedormdl_updated', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='clsciudadesmdl',
            name='department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_configuracion.clsdepartamentosmdl'),
        ),
        migrations.AddField(
            model_name='clsciudadesmdl',
            name='user_creation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modulo_configuracion_clsciudadesmdl_creation', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='clsciudadesmdl',
            name='user_update',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modulo_configuracion_clsciudadesmdl_updated', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='clscategoriaproductomdl',
            name='user_creation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modulo_configuracion_clscategoriaproductomdl_creation', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='clscategoriaproductomdl',
            name='user_update',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modulo_configuracion_clscategoriaproductomdl_updated', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='clscategoriaclientemdl',
            name='user_creation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modulo_configuracion_clscategoriaclientemdl_creation', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='clscategoriaclientemdl',
            name='user_update',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modulo_configuracion_clscategoriaclientemdl_updated', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='clscatalogoproveedoresmdl',
            name='city',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_configuracion.clsciudadesmdl'),
        ),
        migrations.AddField(
            model_name='clscatalogoproveedoresmdl',
            name='department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_configuracion.clsdepartamentosmdl'),
        ),
        migrations.AddField(
            model_name='clscatalogoproveedoresmdl',
            name='user_creation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modulo_configuracion_clscatalogoproveedoresmdl_creation', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='clscatalogoproveedoresmdl',
            name='user_update',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modulo_configuracion_clscatalogoproveedoresmdl_updated', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='clscatalogoproductosmdl',
            name='product_cat',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_configuracion.clscategoriaproductomdl', verbose_name='Categoría'),
        ),
        migrations.AddField(
            model_name='clscatalogoproductosmdl',
            name='product_subcat',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_configuracion.clssubcategoriaproductomdl', verbose_name='Subcategoría'),
        ),
        migrations.AddField(
            model_name='clscatalogoproductosmdl',
            name='purchase_unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_configuracion.clsunidadcompramdl', verbose_name='Unidad de compra'),
        ),
        migrations.AddField(
            model_name='clscatalogoproductosmdl',
            name='sales_unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_configuracion.clsunidadventamdl', verbose_name='Unidad de venta'),
        ),
        migrations.AddField(
            model_name='clscatalogoproductosmdl',
            name='user_creation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modulo_configuracion_clscatalogoproductosmdl_creation', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='clscatalogoproductosmdl',
            name='user_update',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modulo_configuracion_clscatalogoproductosmdl_updated', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='clscatalogoclientesmdl',
            name='city',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_configuracion.clsciudadesmdl'),
        ),
        migrations.AddField(
            model_name='clscatalogoclientesmdl',
            name='commercial_advisor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_configuracion.clsasesorcomercialmdl'),
        ),
        migrations.AddField(
            model_name='clscatalogoclientesmdl',
            name='customer_cat',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_configuracion.clscategoriaclientemdl'),
        ),
        migrations.AddField(
            model_name='clscatalogoclientesmdl',
            name='customer_zone',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_configuracion.clszonaclientemdl'),
        ),
        migrations.AddField(
            model_name='clscatalogoclientesmdl',
            name='department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_configuracion.clsdepartamentosmdl'),
        ),
        migrations.AddField(
            model_name='clscatalogoclientesmdl',
            name='user_creation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modulo_configuracion_clscatalogoclientesmdl_creation', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='clscatalogoclientesmdl',
            name='user_update',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modulo_configuracion_clscatalogoclientesmdl_updated', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='clscatalogobodegasmdl',
            name='city',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_configuracion.clsciudadesmdl'),
        ),
        migrations.AddField(
            model_name='clscatalogobodegasmdl',
            name='department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_configuracion.clsdepartamentosmdl'),
        ),
        migrations.AddField(
            model_name='clscatalogobodegasmdl',
            name='user_creation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modulo_configuracion_clscatalogobodegasmdl_creation', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='clscatalogobodegasmdl',
            name='user_update',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modulo_configuracion_clscatalogobodegasmdl_updated', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='clsasesorcomercialmdl',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='usuario'),
        ),
        migrations.AddField(
            model_name='clsasesorcomercialmdl',
            name='user_creation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modulo_configuracion_clsasesorcomercialmdl_creation', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='clsasesorcomercialmdl',
            name='user_update',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modulo_configuracion_clsasesorcomercialmdl_updated', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='clsasesorcomercialmdl',
            name='zone',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_configuracion.clszonaclientemdl', verbose_name='Zona'),
        ),
        migrations.AddField(
            model_name='clsajusteinventariomdl',
            name='user_creation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modulo_configuracion_clsajusteinventariomdl_creation', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='clsajusteinventariomdl',
            name='user_update',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modulo_configuracion_clsajusteinventariomdl_updated', to=settings.AUTH_USER_MODEL),
        ),
    ]
