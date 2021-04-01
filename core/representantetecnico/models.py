from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import model_to_dict
from django.utils import timezone

from app.settings import MEDIA_URL
from core.bodega.models import Sustancia, Stock
from core.login.models import User, BaseModel, Persona
from core.representantetecnico.files.read import BASE_REPOSITORY, rearm_url
from core.representantetecnico.files.write import create_folder, create_file
from core.representantetecnico.validators import validate_compras_convocatoria
from core.tecnicolaboratorio.models import Laboratorio


class TipoActividad(models.Model):
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


class EstadoTransaccion(models.Model):
    estado = models.CharField(max_length=100, verbose_name="Estado")
    descripcion = models.CharField(max_length=300, verbose_name="Descripcion", null=True, blank=True)
    is_active = models.BooleanField(default=True, editable=False)

    def __str__(self):
        return str(self.estado)

    def toJSON(self):
        item = {'estado': self.estado, 'descripcion': self.descripcion}
        return item

    class Meta:
        verbose_name = "Estado de transacción"
        verbose_name_plural = "Estado de transacciones"
        db_table = "estado_transaccion"
        ordering = ["id"]


class Solicitud(BaseModel):
    solicitante = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Solicitante")
    laboratorio = models.ForeignKey(Laboratorio, on_delete=models.CASCADE, verbose_name="Laboratorio", null=True)
    tipo_actividad = models.ForeignKey(TipoActividad, on_delete=models.CASCADE, verbose_name="Tipo de actividad")
    nombre_actividad = models.CharField(max_length=150, verbose_name="Nombre de proyecto", null=True)
    responsable_actividad = models.ForeignKey(Persona, on_delete=models.CASCADE,
                                              verbose_name="Responsable de actividad")
    documento_solicitud = models.FileField(upload_to='solicitud/%Y/%m/%d', null=True)
    codigo_solicitud = models.CharField(max_length=50, verbose_name="Codigo de solicitud", null=True)
    fecha_autorizacion = models.DateTimeField(editable=False, null=True)
    estado_solicitud = models.ForeignKey(EstadoTransaccion, on_delete=models.CASCADE, verbose_name="Estados solicitud",
                                         null=True)
    observacion_representante = models.TextField(verbose_name="Observación", null=True, blank=True)
    observacion_bodega = models.TextField(verbose_name="Observación", null=True, blank=True)

    def __str__(self):
        return str(self.id)

    def toJSON(self):
        item = {'id': self.id, 'nombre_actividad': self.nombre_actividad,
                'documento': self.get_doc_solicitud(), 'observacion_representante': self.observacion_representante,
                'observacion_bodega': self.observacion_bodega, 'codigo_solicitud': self.codigo_solicitud}
        if self.fecha_autorizacion is not None:
            item['fecha_autorizacion'] = self.fecha_autorizacion.strftime("%Y-%m-%d %H:%M:%S")
        if self.solicitante is not None:
            item['solicitante'] = self.solicitante.get_user_info()
        if self.estado_solicitud is not None:
            item['estado_solicitud'] = self.estado_solicitud.toJSON()
        if self.laboratorio is not None:
            item['laboratorio'] = self.laboratorio.nombre
        if self.tipo_actividad is not None:
            item['tipo_actividad'] = self.tipo_actividad.__str__()
        if self.responsable_actividad is not None:
            item['responsable_actividad'] = self.responsable_actividad.toJSON()
        item['detallesolicitud'] = []
        if self.solicituddetalle_set is not None:
            for i in self.solicituddetalle_set.all():
                item['detallesolicitud'].append(i.toJSON(ver_solicitud=False))
        return item

    def get_doc_solicitud(self):
        if self.documento_solicitud:
            return '{}{}'.format(MEDIA_URL, self.documento_solicitud)
        return ''

    class Meta:
        verbose_name = "Solicitud"
        verbose_name_plural = "Solicitudes"
        db_table = "solicitud"
        ordering = ["id"]


class SolicitudDetalle(BaseModel):
    solicitud = models.ForeignKey(Solicitud, on_delete=models.CASCADE, verbose_name="Solicitud")
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, verbose_name="Stock", null=True)
    cantidad_solicitada = models.DecimalField(verbose_name="Cantidad solicitada", decimal_places=4, max_digits=8,
                                              null=True, default=0)
    cantidad_entregada = models.DecimalField(verbose_name="Cantidad entregada", decimal_places=4, max_digits=8,
                                             null=True, default=0)
    cantidad_consumida = models.DecimalField(verbose_name="Cantidad consumida", decimal_places=4, max_digits=8,
                                             null=True, default=0)

    def __str__(self):
        return str(self.id)

    def toJSON(self, ver_solicitud=False):
        item = {'id': self.id, 'cantidad_solicitada': self.cantidad_solicitada,
                'cantidad_entregada': self.cantidad_entregada, 'cantidad_consumida': self.cantidad_consumida}
        if self.solicitud is not None:
            if ver_solicitud:
                item['solicitud'] = self.solicitud.toJSON()
        if self.stock is not None:
            item['stock'] = self.stock.toJSON(view_subtance=True, view_stock_substance=True)
        return item

    class Meta:
        verbose_name = "Solicitud Detalle"
        verbose_name_plural = "Solicitud Detalles"
        db_table = "detalle_solicitud"
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


class ComprasPublicas(BaseModel):
    empresa = models.ForeignKey(Proveedor, on_delete=models.CASCADE, verbose_name="Empresa", null=True)
    llegada_bodega = models.DateField(default=timezone.now, verbose_name="Fecha llegada a bodega")
    hora_llegada_bodega = models.TimeField(default=timezone.now, verbose_name="Hora llegada a bodega")
    convocatoria = models.IntegerField(blank=True, null=True, validators=[validate_compras_convocatoria])
    pedido_compras_publicas = models.FileField(upload_to='compras_publicas/%Y/%m/%d', null=True)
    guia_transporte = models.FileField(upload_to='compras_publicas/%Y/%m/%d', null=True)
    factura = models.FileField(upload_to='compras_publicas/%Y/%m/%d', null=True)
    estado_compra = models.ForeignKey(EstadoTransaccion, on_delete=models.CASCADE, verbose_name="Estado de compras",
                                      null=True)
    observacion = models.TextField(verbose_name="Observación", null=True, blank=True)

    def __str__(self):
        return str(self.id)

    def toJSON(self):
        item = {'id': self.id, 'llegada_bodega': self.llegada_bodega, 'hora_llegada_bodega': self.hora_llegada_bodega,
                'convocatoria': self.convocatoria, 'pedido_compras_publicas': self.get_pedido_compras_publicas(),
                'guia_transporte': self.get_guia_transporte(), 'factura': self.get_factura(),
                'observacion': self.observacion}
        if self.empresa is not None:
            item['empresa'] = self.empresa.toJSON()
        else:
            item['empresa'] = Proveedor().toJSON()
        item['detallecompra'] = []
        if self.compraspublicasdetalle_set is not None:
            for i in self.compraspublicasdetalle_set.all():
                item['detallecompra'].append(i.toJSON(rel_compraspublicas=True))
        if self.estado_compra is not None:
            item['estado'] = self.estado_compra.toJSON()
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
    cantidad = models.DecimalField(verbose_name="cantidad", decimal_places=4, max_digits=8, null=True, default=0)

    def __str__(self):
        return str(self.id)

    def toJSON(self, rel_compraspublicas=False):
        item = {'id': self.id, 'cantidad': self.cantidad}
        if rel_compraspublicas is False:
            item['compra'] = self.compra.toJSON()
        if self.stock is not None:
            item['stock'] = self.stock.toJSON(view_subtance=True, view_stock_substance=True)
        return item

    class Meta:
        verbose_name = "Compra Publica Detalle"
        verbose_name_plural = "Compras Publicas Detalles"
        db_table = "detalle_compra_publica"
        ordering = ["id"]


class Mes(models.Model):
    nombre = models.CharField(max_length=20, verbose_name="Nombre del mes")
    numero = models.IntegerField(verbose_name="Numero de mes")

    def __str__(self):
        return str(self.nombre)

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = "Mes"
        verbose_name_plural = "Meses"
        db_table = "mes"
        ordering = ["id"]


class InformesMensuales(BaseModel):
    laboratorista = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="laboratorista")
    laboratorio = models.ForeignKey(Laboratorio, on_delete=models.CASCADE, verbose_name="Laboratorio")
    mes = models.ForeignKey(Mes, on_delete=models.CASCADE, verbose_name="Mes", null=True)
    is_editable = models.BooleanField(default=True, editable=False)

    def __str__(self):
        return str(self.id)

    def toJSON(self):
        item = {'id': self.id, 'editable': self.is_editable}
        if self.laboratorista is not None:
            item['laboratorista'] = self.laboratorista.toJSON()
        if self.laboratorio is not None:
            item['laboratorio'] = self.laboratorio.toJSON()
        if self.laboratorio is not None:
            item['mes'] = self.mes.toJSON()
        return item

    @staticmethod
    def verify_month_exist_with_year(month_id, lab_id):
        if InformesMensuales.objects.filter(
                mes_id=month_id,
                date_creation__year=timezone.now().year,
                laboratorio_id=lab_id
        ).exists():
            return True
        return False

    class Meta:
        verbose_name = "Informe mensual"
        verbose_name_plural = "Informes mensuales"
        db_table = "informes_mensuales"
        ordering = ["id"]


class InformesMensualesDetalle(BaseModel):
    informe = models.ForeignKey(InformesMensuales, on_delete=models.CASCADE, verbose_name="Informe")
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, verbose_name="Stock", null=True)
    cantidad = models.DecimalField(verbose_name="cantidad", decimal_places=4, max_digits=8, null=True, default=0)

    def __str__(self):
        return str(self.id)

    def toJSON(self, ver_informe=False):
        item = {'id': self.id, 'cantidad': self.cantidad}
        if ver_informe:
            item['informe'] = self.informe.toJSON()
        if self.stock is not None:
            item['stock'] = self.stock.toJSON(view_subtance=True, view_stock_substance=True)
        return item

    class Meta:
        verbose_name = "Informe mensual Detalle"
        verbose_name_plural = "Informes mensuales Detalles"
        db_table = "detalle_informe_mensual"
        ordering = ["id"]


class DesgloseInfomeMensualDetalle(BaseModel):
    informe_mensual_detalle = models.ForeignKey(InformesMensualesDetalle, on_delete=models.CASCADE, null=True)
    documento = models.FileField(upload_to='informemensual/sustancias/desglose/%Y/%m/%d', null=True)
    solicitud_detalle = models.ForeignKey(SolicitudDetalle, on_delete=models.CASCADE, null=True, blank=True)
    cantidad = models.DecimalField(verbose_name="cantidad", decimal_places=4, max_digits=8, null=True, default=0)

    def __str__(self):
        return str(self.id)

    def toJSON(self):
        item = {"id": self.id, "documento": self.get_documento()}
        if self.informe_mensual_detalle is not None:
            item["informe_mensual_detalle"] = self.informe_mensual_detalle.id
        return item

    def get_documento(self):
        if self.documento:
            return '{}{}'.format(MEDIA_URL, self.documento)
        return ''

    class Meta:
        verbose_name = "Desglose mensual"
        verbose_name_plural = "Desgloses mesuales"
        db_table = "desglose_detalle_informe_mensual"
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
