# Generated by Django 3.1.5 on 2021-02-24 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('representantetecnico', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='compraspublicas',
            name='responsable_entrega',
        ),
        migrations.RemoveField(
            model_name='compraspublicas',
            name='transportista',
        ),
        migrations.AddField(
            model_name='compraspublicas',
            name='pedido_compras_publicas',
            field=models.FileField(blank=True, null=True, upload_to='compras_publicas/%Y/%m/%d'),
        ),
    ]