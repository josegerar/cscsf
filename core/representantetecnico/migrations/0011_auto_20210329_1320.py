# Generated by Django 3.1.5 on 2021-03-29 18:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('representantetecnico', '0010_auto_20210328_1234'),
    ]

    operations = [
        migrations.CreateModel(
            name='DesgloseInfomeMensualDetalle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_creation', models.DateTimeField(auto_now_add=True, null=True)),
                ('date_updated', models.DateTimeField(auto_now=True, null=True)),
                ('documento', models.FileField(null=True, upload_to='documentos/%Y/%m/%d')),
                ('cantidad', models.DecimalField(decimal_places=4, max_digits=8, null=True, verbose_name='cantidad')),
                ('informe_mensual_detalle', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='representantetecnico.informesmensualesdetalle')),
                ('solicitud', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='representantetecnico.solicitud')),
                ('user_creation', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_creation_representantetecnico_desgloseinfomemensualdetalle', to=settings.AUTH_USER_MODEL)),
                ('user_updated', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_updated_representantetecnico_desgloseinfomemensualdetalle', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Desglose mensual',
                'verbose_name_plural': 'Desgloses mesuales',
                'db_table': 'desglose_detalle_informe_mensual',
                'ordering': ['id'],
            },
        ),
        migrations.DeleteModel(
            name='Documento',
        ),
        migrations.DeleteModel(
            name='TipoDocumento',
        ),
    ]