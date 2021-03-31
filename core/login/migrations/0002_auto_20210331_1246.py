# Generated by Django 3.1.5 on 2021-03-31 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='persona',
            name='is_info_update',
            field=models.BooleanField(default=False, editable=False),
        ),
        migrations.AddField(
            model_name='user',
            name='codeconfirm',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='is_pass_update',
            field=models.BooleanField(default=False, editable=False),
        ),
    ]
