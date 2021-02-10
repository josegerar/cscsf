# Create your models here.
from django.db import models
from django.forms import model_to_dict
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

from cssf.files.read import *
from cssf.files.write import create_folder, create_file
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

class TipoPersona(models.Model):
    nombre = models.CharField(max_length=30, verbose_name="Tipo de persona", unique=True)
    descripcion = models.CharField(max_length=200, verbose_name="Descripcion", blank=True, null=True)
    is_active = models.BooleanField(default=True, editable=False)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "TipoPersona"
        verbose_name_plural = "TipoPersonas"
        db_table = "tipo_persona"
        ordering = ["id"]

class Persona(models.Model):
    tipo_persona = models.ForeignKey(TipoPersona, on_delete=models.CASCADE,
                                     null=True, blank=True, verbose_name="Tipo de persona")
    nombre = models.CharField(max_length=100, verbose_name="Nombres", default="")
    apellido = models.CharField(max_length=100, verbose_name="Apellidos")
    cedula = models.CharField(max_length=100, verbose_name="Cedula", unique=True)
    is_active = models.BooleanField(default=True, editable=False)

    def __str__(self):
        return self.nombre + " " + self.apellido

    def toJSON(self):
        item = model_to_dict(self)
        item['tipo'] = self.tipo_persona.nombre
        return item

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
    solicitante = models.ForeignKey(User, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
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
    tecnico = models.ForeignKey(User, on_delete=models.CASCADE)
    laboratorio = models.ForeignKey(Laboratorio, on_delete=models.CASCADE)
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
    is_active = models.BooleanField(default=True, editable=False)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"
        db_table = "proveedor"
        ordering = ["id"]

class ComprasPublicas(models.Model):
    empresa = models.ForeignKey(Proveedor, on_delete=models.CASCADE, verbose_name="Empresa", null=True, blank=True)
    llegada_bodega = models.DateField(default=timezone.now, verbose_name="Fecha llegada a bodega")
    hora_llegada_bodega = models.TimeField(default=timezone.now, verbose_name="Hora llegada a bodega")
    convocatoria = models.IntegerField(blank=True, null=True, validators=[validate_compras_convocatoria])
    responsable_entrega = models.ForeignKey(Persona, on_delete=models.CASCADE, blank=True, null=True,
                                            verbose_name="Responsable entrega", related_name="responsable_entrega")
    transportista = models.ForeignKey(Persona, on_delete=models.CASCADE, blank=True, null=True,
                                      verbose_name="Transportista", related_name="transportista")
    fecha_registro = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "CompraPublica"
        verbose_name_plural = "ComprasPublicas"
        db_table = "compras_publicas"
        ordering = ["id"]

class SolicitanteCompra(models.Model):
    solicitante_compra = models.ForeignKey(User, on_delete=models.CASCADE)
    ingreso_compra = models.ForeignKey(ComprasPublicas, on_delete=models.CASCADE)
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
    solicitud = models.ForeignKey(Solicitud, on_delete=models.PROTECT, blank=True, null=True)
    compra_publica = models.ForeignKey(ComprasPublicas, on_delete=models.PROTECT, blank=True, null=True)
    tipo_documento = models.ForeignKey(TipoDocumento, on_delete=models.CASCADE, blank=True, null=True)
    url_documento = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "Documento"
        verbose_name_plural = "Documentos"
        db_table = "documento"
        ordering = ["id"]

class Entrega(models.Model):
    documento = models.ForeignKey(Documento, on_delete=models.PROTECT)
    ingreso_compras = models.ForeignKey(ComprasPublicas, on_delete=models.PROTECT)
    laboratorio_entrega = models.ForeignKey(Laboratorio, on_delete=models.PROTECT)
    fecha_solicitud_entrega = models.DateTimeField(default=timezone.now, editable=False)
    fecha_entrega = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "Entrega"
        verbose_name_plural = "Entregas"
        db_table = "entrega"
        ordering = ["id"]

class Repositorio(models.Model):
    nombre_usuario = models.CharField(max_length=500, verbose_name="Nombre archivo(usuario)")
    nombre_real = models.CharField(max_length=500, verbose_name="Nombre archivo(real)")
    url = models.CharField(max_length=500, verbose_name="Ruta archivo")
    is_deleted = models.BooleanField(default=False)
    is_recicle_bin = models.BooleanField(default=False)
    is_file = models.BooleanField(default=False)
    is_dir = models.BooleanField(default=False)

    def __str__(self):
        return str(self.url)

    def get_content_folder(self, pk):
        path = None
        if pk == None:
            path = BASE_REPOSITORY
        else:
            objfolder = Repositorio.objects.get(id=pk)
            path = objfolder.url + objfolder.nombre_real + '\\'
        return self.get_content_folder_url(path)

    def get_content_folder_url(self, path_url):
        data = {}
        data_folders = Repositorio.objects.filter(url=path_url).exclude(is_file=True)
        data['folders'] = []
        for i in data_folders:
            data['folders'].append(i.toJSON())
        data_files = Repositorio.objects.filter(url=path_url).exclude(is_dir=True)
        data['files'] = []
        for i in data_files:
            data['files'].append(i.toJSON())
        return data

    def create_folder(self, folderName, pk):
        folder_parent = self.get_folder_parent(pk)
        create_folder(name_folder=folderName, folder_parent=folder_parent)
        self.nombre_real = folderName
        self.nombre_usuario = folderName
        self.url = folder_parent
        self.folder = folder_parent
        self.is_dir = True
        self.save()

    def create_file(self, fileUpload, pk):
        folder_parent = self.get_folder_parent(pk)
        create_file(fileUpload, folder_parent)
        self.nombre_real = fileUpload.name
        self.nombre_usuario = fileUpload.name
        self.url = folder_parent
        self.folder = folder_parent
        self.is_file = True
        self.save()

    def get_folder_parent(self, pk):
        folder_parent = None
        if pk == None:
            folder_parent = BASE_REPOSITORY
        else:
            objectroot = Repositorio.objects.get(pk=pk)
            path = objectroot.url + objectroot.nombre_real + '\\'
            folder_parent = path
        return folder_parent

    def toJSON(self):
        item = model_to_dict(self, exclude=[])
        return item

    class Meta:
        verbose_name = "Repositorio"
        verbose_name_plural = "Repositorios"
        db_table = "repositorio"
        ordering = ["id"]
