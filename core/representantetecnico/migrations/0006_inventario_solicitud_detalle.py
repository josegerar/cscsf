# Generated by Django 3.1.5 on 2021-04-08 21:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('representantetecnico', '0005_compraspublicas_bodega'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventario',
            name='solicitud_detalle',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='representantetecnico.solicituddetalle'),
        ),
    ]
