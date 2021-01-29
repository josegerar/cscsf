# Create your models here.
from django.db import models
from django.forms import model_to_dict
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

from cssf.validators import *


class User(AbstractUser):
    cedula = models.CharField(max_length=10, verbose_name="Cedula", unique=True)
    telefono = models.CharField(max_length=10, verbose_name="Telefono")
    is_representante = models.BooleanField(default=False)
    is_laboratorista = models.BooleanField(default=False)
    is_bodeguero = models.BooleanField(default=False)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
        db_table = "auth_user"
        ordering = ["id"]


class Persona(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombres"),
    apellido = models.CharField(max_length=100, verbose_name="Apellidos")
    cedula = models.CharField(max_length=100, verbose_name="Cedula", unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre + " " + self.apellido

    class Meta:
        verbose_name = "Persona"
        verbose_name_plural = "Personas"
        db_table = "persona"
        ordering = ["id"]


class Categoria(models.Model):
    nombre = models.CharField(max_length=20, verbose_name="Nombre de la categoria", unique=True)
    descripcion = models.CharField(max_length=200, blank=True, null=True)
    is_active = models.BooleanField(default=True, editable=False)
    fecha_creacion = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
        db_table = "categoria"
        ordering = ["id"]


class Solicitud(models.Model):
    id_solicitante_solicitud = models.ForeignKey(User, on_delete=models.CASCADE,
                                                 related_name="id_solicitante_solicitud")
    id_categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name="id_categoria")
    fecha_solicitud = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "Solicitud"
        verbose_name_plural = "Solicitudes"
        db_table = "solicitud"
        ordering = ["id"]


class Laboratorio(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre de laboratorio", unique=True)
    fecha_creacion = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return self.nombre

    def toJSON(self):
        item = model_to_dict(self, exclude=[])
        return item

    class Meta:
        verbose_name = "Laboratorio"
        verbose_name_plural = "Laboratorios"
        db_table = "laboratorio"
        ordering = ["id"]


class TecnicoLaboratorio(models.Model):
    id_tecnico = models.ForeignKey(User, on_delete=models.CASCADE, related_name="id_tecnico")
    id_laboratorio_tecnico = models.ForeignKey(Laboratorio, on_delete=models.CASCADE,
                                               related_name="id_laboratorio_tecnico")
    fecha_asignacion = models.DateTimeField(default=timezone.now, editable=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.id_tecnico.first_name + " - " + self.id_laboratorio.nombre

    class Meta:
        verbose_name = "TecnicoLaboratorio"
        verbose_name_plural = "TecnicosLaboratorios"
        db_table = "tecnico_laboratorio"
        ordering = ["id"]


class Facultad(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre de facultad", unique=True)
    is_active = models.BooleanField(default=True, editable=False)
    fecha_creacion = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Facultad"
        verbose_name_plural = "Facultades"
        db_table = "facultad"
        ordering = ["id"]


class Proveedor(models.Model):
    nombre = models.CharField(max_length=150, verbose_name="Nombre de empresa")
    ruc = models.CharField(max_length=13, verbose_name="Ruc", unique=True)
    id_responsable_entrega_proveedor = models.ForeignKey(Persona, on_delete=models.CASCADE, blank=True, null=True,
                                                         related_name="id_responsable_entrega_proveedor")
    id_transportista_proveedor = models.ForeignKey(Persona, on_delete=models.CASCADE, blank=True, null=True,
                                                   related_name="id_transportista_proveedor")
    is_active = models.BooleanField(default=True, editable=False)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"
        db_table = "proveedor"
        ordering = ["id"]


class ComprasPublicas(models.Model):
    id_empresa = models.ForeignKey(Proveedor, on_delete=models.CASCADE, related_name="id_empresa",
                                   verbose_name="Empresa")
    llegada_bodega = models.DateField(default=timezone.now, verbose_name="Fecha llegada a bodega")
    hora_llegada_bodega = models.TimeField(default=timezone.now, verbose_name="Hora llegada a bodega")
    convocatoria = models.IntegerField(blank=True, null=True, validators=[validate_compras_convocatoria])
    id_responsable_entrega_compras = models.ForeignKey(Persona, on_delete=models.CASCADE, blank=True, null=True,
                                                       related_name="id_responsable_entrega_compras",
                                                       verbose_name="Responsable entrega")
    id_transportista_compras = models.ForeignKey(Persona, on_delete=models.CASCADE, blank=True, null=True,
                                                 related_name="id_transportista_compras", verbose_name="Transportista")
    fecha_registro = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "CompraPublica"
        verbose_name_plural = "ComprasPublicas"
        db_table = "compras_publicas"
        ordering = ["id"]


class SolicitanteCompra(models.Model):
    id_solicitante_compra = models.ForeignKey(User, on_delete=models.CASCADE, related_name="id_solicitante_compra")
    id_ingreso_compra = models.ForeignKey(ComprasPublicas, on_delete=models.CASCADE, related_name="id_ingreso_compra")
    tipo_sc = models.CharField(max_length=2, null=True, validators=[validate_solicitante_compra_tipo_sc])

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "SolicitanteCompra"
        verbose_name_plural = "SolicitantesCompras"
        db_table = "solicitante_compra"
        ordering = ["id"]


class TipoDocumento(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    descripcion = models.CharField(max_length=300, verbose_name="Descripcion")
    is_active = models.BooleanField(default=True, editable=False)

    def __str__(self):
        return str(self.nombre)

    class Meta:
        verbose_name = "TipoDocumento"
        verbose_name_plural = "TipoDocumentos"
        db_table = "tipo_documento"
        ordering = ["id"]


class Documento(models.Model):
    id_solicitud = models.ForeignKey(Solicitud, on_delete=models.PROTECT, blank=True, null=True,
                                     related_name="id_solicitud")
    id_compra_publica = models.ForeignKey(ComprasPublicas, on_delete=models.PROTECT, blank=True, null=True,
                                          related_name="id_compra_publica")
    id_tipo_documento = models.ForeignKey(TipoDocumento, on_delete=models.CASCADE, blank=True, null=True,
                                          related_name="id_tipo_documento")
    url_documento = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "Documento"
        verbose_name_plural = "Documentos"
        db_table = "documento"
        ordering = ["id"]


class Entrega(models.Model):
    id_documento = models.ForeignKey(Documento, on_delete=models.PROTECT, related_name="id_documento")
    id_ingreso_compras = models.ForeignKey(ComprasPublicas, on_delete=models.PROTECT, related_name="id_ingreso_compras")
    id_laboratorio_entrega = models.ForeignKey(Laboratorio, on_delete=models.PROTECT,
                                               related_name="id_laboratorio_entrega")
    fecha_solicitud_entrega = models.DateTimeField(default=timezone.now, editable=False)
    fecha_entrega = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "Entrega"
        verbose_name_plural = "Entregas"
        db_table = "entrega"
        ordering = ["id"]
