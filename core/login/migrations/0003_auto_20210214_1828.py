# Generated by Django 3.1.5 on 2021-02-14 23:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0002_auto_20210214_1826'),
    ]

    operations = [
        migrations.AddField(
            model_name='grocerprofile',
            name='date_creation',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='grocerprofile',
            name='date_updated',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='grocerprofile',
            name='user_creation',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_creation_login_grocerprofile', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='grocerprofile',
            name='user_updated',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_updated_login_grocerprofile', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='laboratoryworkerprofile',
            name='date_creation',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='laboratoryworkerprofile',
            name='date_updated',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='laboratoryworkerprofile',
            name='user_creation',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_creation_login_laboratoryworkerprofile', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='laboratoryworkerprofile',
            name='user_updated',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_updated_login_laboratoryworkerprofile', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='representativeprofile',
            name='date_creation',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='representativeprofile',
            name='date_updated',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='representativeprofile',
            name='user_creation',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_creation_login_representativeprofile', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='representativeprofile',
            name='user_updated',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_updated_login_representativeprofile', to=settings.AUTH_USER_MODEL),
        ),
    ]
