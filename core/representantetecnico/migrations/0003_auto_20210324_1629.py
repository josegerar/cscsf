# Generated by Django 3.1.5 on 2021-03-24 21:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('representantetecnico', '0002_auto_20210324_1322'),
    ]

    operations = [
        migrations.AddField(
            model_name='compraspublicas',
            name='observacion',
            field=models.TextField(blank=True, null=True, verbose_name='Observación'),
        ),
        migrations.AddField(
            model_name='solicitud',
            name='observacion',
            field=models.TextField(blank=True, null=True, verbose_name='Observación'),
        ),
    ]
