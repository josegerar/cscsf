# Generated by Django 3.1.5 on 2021-03-22 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('representantetecnico', '0009_remove_compraspublicasdetalle_cantidad'),
    ]

    operations = [
        migrations.AddField(
            model_name='compraspublicasdetalle',
            name='cantidad',
            field=models.DecimalField(decimal_places=4, max_digits=8, null=True, verbose_name='cantidad'),
        ),
    ]