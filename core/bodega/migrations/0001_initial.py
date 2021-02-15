# Generated by Django 3.1.5 on 2021-02-14 23:22

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TipoPresentacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=10, verbose_name='Nombre de tipo de presentacion')),
                ('descripcion', models.CharField(max_length=10, verbose_name='Descripción de tipo de presentacion')),
            ],
            options={
                'verbose_name': 'TipoPresentacion',
                'verbose_name_plural': 'TipoPresentaciones',
                'db_table': 'tipo_presentacion',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Sustancia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, unique=True, verbose_name='Nombre de sustancia')),
                ('cantidad', models.IntegerField(default=0, verbose_name='Cantidad actal de sustancias')),
                ('tipo_presentacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bodega.tipopresentacion', verbose_name='TIpo de presentacion')),
            ],
            options={
                'verbose_name': 'Sustancia',
                'verbose_name_plural': 'Sustancias',
                'db_table': 'sustancia',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Inventario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad_movimiento', models.IntegerField(default=0, verbose_name='Cantidad movimiento')),
                ('fecha_movimiento', models.DateField(default=django.utils.timezone.now)),
                ('sustancia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bodega.sustancia', verbose_name='Sustancia')),
            ],
            options={
                'verbose_name': 'Inventario',
                'verbose_name_plural': 'Inventarios',
                'db_table': 'inventario',
                'ordering': ['id'],
            },
        ),
    ]