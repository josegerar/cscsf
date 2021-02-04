# Generated by Django 3.1.5 on 2021-02-03 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cssf', '0002_auto_20210201_2211'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='repositorio',
            name='folder',
        ),
        migrations.AlterField(
            model_name='repositorio',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='repositorio',
            name='is_dir',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='repositorio',
            name='is_file',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='repositorio',
            name='is_recicle_bin',
            field=models.BooleanField(default=False),
        ),
    ]
