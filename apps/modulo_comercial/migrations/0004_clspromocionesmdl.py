# Generated by Django 3.1.1 on 2022-03-18 17:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('modulo_comercial', '0003_auto_20220318_0940'),
    ]

    operations = [
        migrations.CreateModel(
            name='clsPromocionesMdl',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('update_date', models.DateTimeField(auto_now=True, null=True)),
                ('promotion_name', models.CharField(max_length=200, verbose_name='Promoción')),
                ('user_creation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modulo_comercial_clspromocionesmdl_creation', to=settings.AUTH_USER_MODEL)),
                ('user_update', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modulo_comercial_clspromocionesmdl_updated', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Promoción',
                'verbose_name_plural': 'Promociones',
                'ordering': ['id'],
            },
        ),
    ]