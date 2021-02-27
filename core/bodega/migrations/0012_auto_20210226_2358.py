# Generated by Django 3.1.5 on 2021-02-27 04:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tecnicolaboratorio', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bodega', '0011_auto_20210226_1017'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inventario',
            name='bodega',
        ),
        migrations.RemoveField(
            model_name='inventario',
            name='sustancia',
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_creation', models.DateTimeField(auto_now_add=True, null=True)),
                ('date_updated', models.DateTimeField(auto_now=True, null=True)),
                ('cantidad', models.DecimalField(decimal_places=4, max_digits=9)),
                ('bodega', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='bodega.bodega')),
                ('laboratorio', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tecnicolaboratorio.laboratorio')),
                ('sustancia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bodega.sustancia')),
                ('user_creation', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_creation_bodega_stock', to=settings.AUTH_USER_MODEL)),
                ('user_updated', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_updated_bodega_stock', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Stock sustancia',
                'verbose_name_plural': 'Stock sustancias',
                'db_table': 'stock',
                'ordering': ['id'],
            },
        ),
        migrations.AddField(
            model_name='inventario',
            name='stock',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='bodega.stock', verbose_name='Stock de sustancia'),
        ),
    ]
