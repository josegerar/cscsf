from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import model_to_dict
from django.utils import timezone

from app.settings import MEDIA_URL
from core.bodega.models import Sustancia, Stock
from core.login.models import User, BaseModel
from core.representantetecnico.files.read import *
from core.representantetecnico.files.write import *
from core.representantetecnico.validators import *
from core.tecnicolaboratorio.models import Laboratorio


class TipoPersona(BaseModel):
    nombre = models.CharField(max_length=30, verbose_name="Tipo de persona", unique=True)
    descripcion = models.CharField(max_length=200, verbose_name="Descripcion", blank=True, null=True)
    is_active = models.BooleanField(default=True, editable=False)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Tipo de persona"
        verbose_name_plural = "Tipos de Personas"
        db_table = "tipo_persona"
        ordering = ["id"]


class Persona(BaseModel):
    tipo_persona = models.ForeignKey(TipoPersona, on_delete=models.CASCADE,
                                     null=True, blank=True, verbose_name="Tipo de persona")
    nombre = models.CharField(max_length=100, verbose_name="Nombres", default="")
    apellido = models.CharField(max_length=100, verbose_name="Apellidos")
    cedula = models.CharField(max_length=10, verbose_name="Cedula", unique=True)
    is_active = models.BooleanField(default=True, editable=False)

    def __str__(self):
        return self.nombre + " " + self.apellido

    def toJSON(self):
        item = model_to_dict(self, exclude=['tipo_persona'])
        if self.tipo_persona is not None:
            item['tipo'] = self.tipo_persona.nombre
        else:
            item['tipo'] = ""
        return item

    class Meta:
        verbose_name = "Persona"
        verbose_name_plural = "Personas"
        db_table = "persona"
        ordering = ["id"]


class Categoria(BaseModel):
    nombre = models.CharField(max_length=20, verbose_name="Nombre de la categoria", unique=True)
    descripcion = models.CharField(max_length=200, blank=True, null=True)
    is_active = models.BooleanField(default=True, editable=False)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
        db_table = "categoria"
        ordering = ["id"]


class TipoActividad(BaseModel):
    nombre = models.CharField(max_length=20, verbose_name="Nombre", unique=True)
    descripcion = models.CharField(max_length=200, blank=True, null=True, verbose_name="Descripcion")
    is_active = models.BooleanField(default=True, editable=False)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Tipo de actividad"
        verbose_name_plural = "Tipos de actividades"
        db_table = "tipo_actividad"
        ordering = ["id"]


class Solicitud(BaseModel):
    solicitante = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Solicitante")
    laboratorio = models.ForeignKey(Laboratorio, on_delete=models.CASCADE, verbose_name="Laboratorio", null=True)
    tipo_actividad = models.ForeignKey(TipoActividad, on_delete=models.CASCADE, verbose_name="Tipo de actividad")
    nombre_actividad = models.CharField(max_length=150, verbose_name="Nombre de proyecto", null=True)
    responsable_actividad = models.ForeignKey(Persona, on_delete=models.CASCADE,
                                              verbose_name="Responsable de actividad")
    documento_solicitud = models.FileField(upload_to='solicitud/%Y/%m/%d', null=True, blank=True)
    is_autorized = models.BooleanField(default=False, verbose_name="Autorizada", null=True)
    fecha_autorizacion = models.DateTimeField(editable=False, null=True)

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        if self.is_autorized is True:
            if self.fecha_autorizacion is None:
                self.fecha_autorizacion = timezone.now()
        else:
            if self.fecha_autorizacion is not None:
                self.fecha_autorizacion = None
        super().save(*args, **kwargs)

    def toJSON(self):
        item = {'id': self.id, 'nombre_actividad': self.nombre_actividad,
                'documento': self.get_doc_solicitud(), 'autorizacion': self.get_autorizacion(),
                'fecha_autorizacion': self.fecha_autorizacion.strftime("%Y-%m-%d %H:%M:%S")}
        if self.solicitante is not None:
            item['solicitante'] = self.solicitante.get_user_info()
        else:
            item['solicitante'] = ""
        if self.laboratorio is not None:
            item['laboratorio'] = self.laboratorio.nombre
        else:
            item['laboratorio'] = ""
        if self.tipo_actividad is not None:
            item['tipo_actividad'] = self.tipo_actividad.__str__()
        else:
            item['tipo_actividad'] = ""
        if self.responsable_actividad is not None:
            item['responsable_actividad'] = self.responsable_actividad
        else:
            item['responsable_actividad'] = ""
        return item

    def get_doc_solicitud(self):
        if self.documento_solicitud:
            return '{}{}'.format(MEDIA_URL, self.documento_solicitud)
        return ''

    def get_autorizacion(self):
        if self.is_autorized is True:
            return 'Autorizado'
        else:
            return 'No autorizado'

    class Meta:
        verbose_name = "Solicitud"
        verbose_name_plural = "Solicitudes"
        db_table = "solicitud"
        ordering = ["id"]


class Facultad(BaseModel):
    nombre = models.CharField(max_length=100, verbose_name="Nombre de facultad", unique=True)
    is_active = models.BooleanField(default=True, editable=False)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Facultad"
        verbose_name_plural = "Facultades"
        db_table = "facultad"
        ordering = ["id"]


class Proveedor(BaseModel):
    nombre = models.CharField(max_length=150, verbose_name="Nombre de empresa")
    ruc = models.CharField(max_length=13, verbose_name="Ruc", unique=True)
    is_active = models.BooleanField(default=True, editable=False)

    def __str__(self):
        return self.nombre

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"
        db_table = "proveedor"
        ordering = ["id"]


class EstadoCompra(BaseModel):
    estado = models.CharField(max_length=100, verbose_name="Estado")
    descripcion = models.CharField(max_length=300, verbose_name="Descripcion")
    is_active = models.BooleanField(default=True, editable=False)

    def __str__(self):
        return str(self.estado)

    def toJSON(self):
        item = {'estado':self.estado, 'descripcion':self.descripcion}
        return item

    class Meta:
        verbose_name = "Estado de compra"
        verbose_name_plural = "Estado de compras"
        db_table = "estado_compra"
        ordering = ["id"]


class ComprasPublicas(BaseModel):
    empresa = models.ForeignKey(Proveedor, on_delete=models.CASCADE, verbose_name="Empresa", null=True)
    llegada_bodega = models.DateField(default=timezone.now, verbose_name="Fecha llegada a bodega")
    hora_llegada_bodega = models.TimeField(default=timezone.now, verbose_name="Hora llegada a bodega")
    convocatoria = models.IntegerField(blank=True, null=True, validators=[validate_compras_convocatoria])
    pedido_compras_publicas = models.FileField(upload_to='compras_publicas/%Y/%m/%d', null=True)
    guia_transporte = models.FileField(upload_to='compras_publicas/%Y/%m/%d', null=True)
    factura = models.FileField(upload_to='compras_publicas/%Y/%m/%d', null=True)
    estado_compra = models.ForeignKey(EstadoCompra, on_delete=models.CASCADE, verbose_name="Estado de compras", null=True)

    def __str__(self):
        return str(self.id)

    def toJSON(self):
        item = {'id': self.id, 'llegada_bodega': self.llegada_bodega, 'hora_llegada_bodega': self.hora_llegada_bodega,
                'convocatoria': self.convocatoria, 'pedido_compras_publicas': self.get_pedido_compras_publicas(),
                'guia_transporte': self.get_guia_transporte(), 'factura': self.get_factura()}
        if self.empresa is not None:
            item['empresa'] = self.empresa.toJSON()
        else:
            item['empresa'] = Proveedor().toJSON()
        item['detallecompra'] = []
        if self.compraspublicasdetalle_set is not None:
            for i in self.compraspublicasdetalle_set.all():
                item['detallecompra'].append(i.toJSON(rel_compraspublicas=True))
        if self.estado_compra is not None:
            item ['estado'] = self.estado_compra.toJSON()
        else:
            item['estado'] = EstadoCompra().toJSON()
        return item

    def get_pedido_compras_publicas(self):
        if self.pedido_compras_publicas:
            return '{}{}'.format(MEDIA_URL, self.pedido_compras_publicas)
        return ''

    def get_guia_transporte(self):
        if self.guia_transporte:
            return '{}{}'.format(MEDIA_URL, self.guia_transporte)
        return ''

    def get_factura(self):
        if self.factura:
            return '{}{}'.format(MEDIA_URL, self.factura)
        return ''

    class Meta:
        verbose_name = "Compra Publica"
        verbose_name_plural = "Compras Publicas"
        db_table = "compras_publicas"
        ordering = ["id"]


class ComprasPublicasDetalle(BaseModel):
    compra = models.ForeignKey(ComprasPublicas, on_delete=models.CASCADE, verbose_name="Compra")
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, verbose_name="Stock", null=True)
    cantidad = models.IntegerField(verbose_name="cantidad")

    def __str__(self):
        return str(self.id)

    def toJSON(self, rel_compraspublicas=False):
        item = {'cantidad': self.cantidad}
        if rel_compraspublicas is False:
            item['compra'] = self.compra.toJSON()
        if self.stock is not None:
            item['stock'] = self.stock.toJSON()
        else:
            item['stock'] = Stock().toJSON()
        return item

    class Meta:
        verbose_name = "Compra Publica Detalle"
        verbose_name_plural = "Compras Publicas Detalles"
        db_table = "detalle_compra_publica"
        ordering = ["id"]


class SolicitanteCompra(BaseModel):
    solicitante_compra = models.ForeignKey(User, on_delete=models.CASCADE)
    ingreso_compra = models.ForeignKey(ComprasPublicas, on_delete=models.CASCADE)
    tipo_sc = models.CharField(max_length=2, null=True, validators=[validate_solicitante_compra_tipo_sc])

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "Solicitante Compra"
        verbose_name_plural = "Solicitantes Compras"
        db_table = "solicitante_compra"
        ordering = ["id"]


class TipoDocumento(BaseModel):
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    descripcion = models.CharField(max_length=300, verbose_name="Descripcion")
    is_active = models.BooleanField(default=True, editable=False)

    def __str__(self):
        return str(self.nombre)

    class Meta:
        verbose_name = "Tipo de Documento"
        verbose_name_plural = "Tipos de Documentos"
        db_table = "tipo_documento"
        ordering = ["id"]


class Documento(BaseModel):
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


class Entrega(BaseModel):
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


class Repositorio(BaseModel):
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
        object_act = None
        if pk is None:
            path = BASE_REPOSITORY
        else:
            object_act = Repositorio.objects.get(id=pk)
            path = object_act.url + object_act.nombre_real + '\\'
        return self.get_content_folder_url(path, object_act)

    def get_content_folder_url(self, path_url, object_act):
        data = {}
        if object_act is not None:
            data['object'] = object_act.toJSON()
            if object_act.is_file is True:
                path_url = object_act.url
                if path_url != BASE_REPOSITORY:
                    path_parts = object_act.url.split("\\")
                    folder_name = path_parts[len(path_parts) - 2]
                    path_parent = rearm_url(path_parts, 2)
                    parent = Repositorio.objects.get(nombre_real=folder_name, url=path_parent)
                    data['parent'] = parent.toJSON()
        data_folders = Repositorio.objects.filter(url=path_url).exclude(is_file=True)
        data['folders'] = []
        for i in data_folders:
            data['folders'].append(i.toJSON())
        data_files = Repositorio.objects.filter(url=path_url).exclude(is_dir=True)
        data['files'] = []
        for i in data_files:
            data['files'].append(i.toJSON())
        return data

    def create_folder(self, foldername, pk):
        folder_parent = self.get_folder_parent(pk)
        create_folder(name_folder=foldername, folder_parent=folder_parent)
        self.nombre_real = foldername
        self.nombre_usuario = foldername
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
        if pk is None:
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
