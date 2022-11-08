# Generated by Django 2.0.2 on 2022-07-19 13:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ordenescompra1', '0001_initial'),
        ('v1', '0001_initial'),
        ('productos', '0002_auto_20220715_0403'),
        ('p1', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordencompra1',
            name='proveedor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='p1.P1'),
        ),
        migrations.AddField(
            model_name='ordencompra1',
            name='vendedor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='v1.V1'),
        ),
        migrations.AddField(
            model_name='detalle1',
            name='dato_compra',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ordenescompra1.Ordencompra1'),
        ),
        migrations.AddField(
            model_name='detalle1',
            name='dato_producto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='productos.Producto'),
        ),
    ]
