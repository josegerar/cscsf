# Create your models here.
from django.db import models
from django.utils import timezone

from CSSF.validators import *


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


class Solicitante(models.Model):
    nombre = models.CharField(max_length=25, verbose_name="Nombres del solicitante")
    apellido = models.CharField(max_length=25, verbose_name="Apellidos del solicitante")
    cedula = models.CharField(max_length=10, verbose_name="Numero de cedula", unique=True)
    telefono = models.CharField(max_length=10, blank=True, null=True, verbose_name="Numero de telefono")
    correo_electronico = models.CharField(max_length=150, verbose_name="Correo electronico", unique=True)
    fecha_creacion = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Solicitante"
        verbose_name_plural = "Solicitantes"
        db_table = "solicitante"
        ordering = ["id"]


class Solicitud(models.Model):
    id_solicitante = models.ForeignKey(Solicitante, on_delete=models.PROTECT)
    id_categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)
    fecha_solicitud = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return self.id

    class Meta:
        verbose_name = "Solicitud"
        verbose_name_plural = "Solicitudes"
        db_table = "solicitud"
        ordering = ["id"]


class Laboratorio(models.Model):
    id_solicitante = models.ForeignKey(Solicitante, on_delete=models.PROTECT)
    nombre = models.CharField(max_length=100, verbose_name="Nombre de laboratorio", unique=True)
    fecha_creacion = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Laboratorio"
        verbose_name_plural = "Laboratorios"
        db_table = "labratorio"
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


class IngresoCompras(models.Model):
    id_facultad = models.ForeignKey(Facultad, on_delete=models.PROTECT)
    nombre_proyecto = models.CharField(max_length=200, verbose_name="Nombre de proyecto")
    convocatoria = models.IntegerField(blank=True, null=True, validators=[validate_compras_convocatoria])

    def __str__(self):
        return self.id

    class Meta:
        verbose_name = "IngresoCompra"
        verbose_name_plural = "IngresosCompras"
        db_table = "ingreso_compra"
        ordering = ["id"]

class SolicitanteCompra(models.Model):
    id_solicitante = models.ForeignKey(Solicitante, on_delete=models.PROTECT)
    id_ingreso_compra = models.ForeignKey(IngresoCompras, on_delete=models.PROTECT)
    tipo_sc = models.CharField(max_length=2, null=True, validators=[validate_solicitante_compra_tipo_sc])

    def __str__(self):
        return self.id

    class Meta:
        verbose_name = "SolicitanteCompra"
        verbose_name_plural = "SolicitantesCompras"
        db_table = "solicitante_compra"
        ordering = ["id"]

class Documento(models.Model):
    id_solicitud = models.ForeignKey(Solicitud, on_delete=models.PROTECT)
    id_ingreso_compras = models.ForeignKey(IngresoCompras, on_delete=models.PROTECT)
    url_documento = models.CharField(max_length=200, unique=True)
    tipo_documento = models.CharField(max_length=100)

    def __str__(self):
        return self.id

    class Meta:
        verbose_name = "Documento"
        verbose_name_plural = "Documentos"
        db_table = "documento"
        ordering = ["id"]

class Entrega(models.Model):
    id_documento = models.ForeignKey(Documento, on_delete=models.PROTECT)
    id_ingreso_compras = models.ForeignKey(IngresoCompras, on_delete=models.PROTECT)
    id_laboratorio = models.ForeignKey(Laboratorio, on_delete=models.PROTECT)
    fecha_solicitud_entrega = models.DateTimeField(timezone.now, editable=False)
    fecha_entrega = models.DateTimeField(timezone.now, editable=False)

    def __str__(self):
        return self.id

    class Meta:
        verbose_name = "Entrega"
        verbose_name_plural = "Entregas"
        db_table = "entrega"
        ordering = ["id"]

