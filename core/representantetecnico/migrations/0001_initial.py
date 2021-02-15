# Generated by Django 3.1.5 on 2021-02-14 23:22

import core.representantetecnico.validators
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tecnicolaboratorio', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=20, unique=True, verbose_name='Nombre de la categoria')),
                ('descripcion', models.CharField(blank=True, max_length=200, null=True)),
                ('is_active', models.BooleanField(default=True, editable=False)),
                ('fecha_creacion', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
            ],
            options={
                'verbose_name': 'Categoria',
                'verbose_name_plural': 'Categorias',
                'db_table': 'categoria',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='ComprasPublicas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('llegada_bodega', models.DateField(default=django.utils.timezone.now, verbose_name='Fecha llegada a bodega')),
                ('hora_llegada_bodega', models.TimeField(default=django.utils.timezone.now, verbose_name='Hora llegada a bodega')),
                ('convocatoria', models.IntegerField(blank=True, null=True, validators=[core.representantetecnico.validators.validate_compras_convocatoria])),
                ('fecha_registro', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('guia_transporte', models.FileField(blank=True, null=True, upload_to='compras_publicas/%Y/%m/%d')),
                ('factura', models.FileField(blank=True, null=True, upload_to='compras_publicas/%Y/%m/%d')),
            ],
            options={
                'verbose_name': 'CompraPublica',
                'verbose_name_plural': 'ComprasPublicas',
                'db_table': 'compras_publicas',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Documento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url_documento', models.CharField(max_length=200, unique=True)),
                ('compra_publica', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='representantetecnico.compraspublicas')),
            ],
            options={
                'verbose_name': 'Documento',
                'verbose_name_plural': 'Documentos',
                'db_table': 'documento',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Facultad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, unique=True, verbose_name='Nombre de facultad')),
                ('is_active', models.BooleanField(default=True, editable=False)),
                ('fecha_creacion', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
            ],
            options={
                'verbose_name': 'Facultad',
                'verbose_name_plural': 'Facultades',
                'db_table': 'facultad',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Proveedor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=150, verbose_name='Nombre de empresa')),
                ('ruc', models.CharField(max_length=13, unique=True, verbose_name='Ruc')),
                ('is_active', models.BooleanField(default=True, editable=False)),
            ],
            options={
                'verbose_name': 'Empresa',
                'verbose_name_plural': 'Empresas',
                'db_table': 'proveedor',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Repositorio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_usuario', models.CharField(max_length=500, verbose_name='Nombre archivo(usuario)')),
                ('nombre_real', models.CharField(max_length=500, verbose_name='Nombre archivo(real)')),
                ('url', models.CharField(max_length=500, verbose_name='Ruta archivo')),
                ('is_deleted', models.BooleanField(default=False)),
                ('is_recicle_bin', models.BooleanField(default=False)),
                ('is_file', models.BooleanField(default=False)),
                ('is_dir', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Repositorio',
                'verbose_name_plural': 'Repositorios',
                'db_table': 'repositorio',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='TipoDocumento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, verbose_name='Nombre')),
                ('descripcion', models.CharField(max_length=300, verbose_name='Descripcion')),
                ('is_active', models.BooleanField(default=True, editable=False)),
            ],
            options={
                'verbose_name': 'TipoDocumento',
                'verbose_name_plural': 'TipoDocumentos',
                'db_table': 'tipo_documento',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='TipoPersona',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_creation', models.DateTimeField(auto_now_add=True, null=True)),
                ('date_updated', models.DateTimeField(auto_now=True, null=True)),
                ('nombre', models.CharField(max_length=30, unique=True, verbose_name='Tipo de persona')),
                ('descripcion', models.CharField(blank=True, max_length=200, null=True, verbose_name='Descripcion')),
                ('is_active', models.BooleanField(default=True, editable=False)),
                ('user_creation', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_creation_representantetecnico_tipopersona', to=settings.AUTH_USER_MODEL)),
                ('user_updated', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_updated_representantetecnico_tipopersona', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'TipoPersona',
                'verbose_name_plural': 'TipoPersonas',
                'db_table': 'tipo_persona',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Solicitud',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_solicitud', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='representantetecnico.categoria')),
                ('solicitante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Solicitud',
                'verbose_name_plural': 'Solicitudes',
                'db_table': 'solicitud',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='SolicitanteCompra',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_sc', models.CharField(max_length=2, null=True, validators=[core.representantetecnico.validators.validate_solicitante_compra_tipo_sc])),
                ('ingreso_compra', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='representantetecnico.compraspublicas')),
                ('solicitante_compra', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'SolicitanteCompra',
                'verbose_name_plural': 'SolicitantesCompras',
                'db_table': 'solicitante_compra',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Persona',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_creation', models.DateTimeField(auto_now_add=True, null=True)),
                ('date_updated', models.DateTimeField(auto_now=True, null=True)),
                ('nombre', models.CharField(default='', max_length=100, verbose_name='Nombres')),
                ('apellido', models.CharField(max_length=100, verbose_name='Apellidos')),
                ('cedula', models.CharField(max_length=10, unique=True, verbose_name='Cedula')),
                ('is_active', models.BooleanField(default=True, editable=False)),
                ('tipo_persona', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='representantetecnico.tipopersona', verbose_name='Tipo de persona')),
                ('user_creation', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_creation_representantetecnico_persona', to=settings.AUTH_USER_MODEL)),
                ('user_updated', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_updated_representantetecnico_persona', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Persona',
                'verbose_name_plural': 'Personas',
                'db_table': 'persona',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Entrega',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_solicitud_entrega', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('fecha_entrega', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('documento', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='representantetecnico.documento')),
                ('ingreso_compras', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='representantetecnico.compraspublicas')),
                ('laboratorio_entrega', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='tecnicolaboratorio.laboratorio')),
            ],
            options={
                'verbose_name': 'Entrega',
                'verbose_name_plural': 'Entregas',
                'db_table': 'entrega',
                'ordering': ['id'],
            },
        ),
        migrations.AddField(
            model_name='documento',
            name='solicitud',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='representantetecnico.solicitud'),
        ),
        migrations.AddField(
            model_name='documento',
            name='tipo_documento',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='representantetecnico.tipodocumento'),
        ),
        migrations.AddField(
            model_name='compraspublicas',
            name='empresa',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='representantetecnico.proveedor', verbose_name='Empresa'),
        ),
        migrations.AddField(
            model_name='compraspublicas',
            name='responsable_entrega',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='responsable_entrega', to='representantetecnico.persona', verbose_name='Responsable entrega'),
        ),
        migrations.AddField(
            model_name='compraspublicas',
            name='transportista',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='transportista', to='representantetecnico.persona', verbose_name='Transportista'),
        ),
    ]