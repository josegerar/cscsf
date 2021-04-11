import json

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import TemplateView

from core.base.mixins import ValidatePermissionRequiredMixin
from core.representantetecnico.models import Solicitud, EstadoTransaccion, TipoMovimientoInventario, Stock, Inventario


class SolicitudView(LoginRequiredMixin, ValidatePermissionRequiredMixin, TemplateView):
    permission_required = ('representantetecnico.view_solicitud',)
    template_name = 'solicitudtl/view.html'
    url_redirect = reverse_lazy('tl:solicitudes')

    def dispatch(self, request, *args, **kwargs):
        try:
            self.object = Solicitud.objects.get(pk=kwargs['pk'])
            return super().dispatch(request, *args, **kwargs)
        except Exception as e:
            messages.error(request, str(e))
        return HttpResponseRedirect(self.url_redirect)

    def get(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.GET.get('action')
            if action is not None:
                if action == 'search_detalle':
                    data = self.search_detalle()
                    return JsonResponse(data, safe=False)
        except Exception as e:
            data['error'] = str(e)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url_list'] = self.url_redirect
        context['icontitle'] = 'eye'
        context['title'] = '{} {}'.format("Solicitud", self.object.id)
        return context

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST.get('action')
            if action is not None:
                if action == 'recibirSolicitud':
                    if request.user.is_laboratory_worker:
                        self.recibir_solicitud()
                    else:
                        data['error'] = 'No tiene permisos'
                elif action == 'aprobarSolicitud':
                    tipoobs = request.POST.get("tipoobs")
                    observacion = request.POST.get('observacion')
                    if request.user.is_representative:
                        self.aprobar_solicitud(tipoobs, observacion)
                    else:
                        data['error'] = 'No tiene permisos'
                elif action == 'revisionSolicitud':
                    tipoobs = request.POST.get("tipoobs")
                    observacion = request.POST.get('observacion')
                    if request.user.is_representative or request.user.is_grocer:
                        self.revision_solicitud(tipoobs, observacion)
                    else:
                        data['error'] = 'No tiene permisos'
                elif action == 'entregarSolicitud':
                    detalle_solicitud = request.POST.get('detalles')
                    observacion_solicitud = request.POST.get('observacion')
                    if request.user.is_grocer:
                        self.entregar_solicitud(detalle_solicitud, observacion_solicitud)
                    else:
                        data['error'] = 'No tiene permisos'
            else:
                data['error'] = 'Faltan datos'
        except Exception as e:
            data["error"] = str(e)
        return JsonResponse(data, safe=False)

    def recibir_solicitud(self):
        with transaction.atomic():
            solicitud = self.object
            estado_solicitud = EstadoTransaccion.objects.get(estado='recibido')
            solicitud.estado_solicitud_id = estado_solicitud.id
            solicitud.save()

    def aprobar_solicitud(self, tipoobs, observacion):
        if tipoobs is not None:
            with transaction.atomic():
                solicitud = self.object
                estado_solicitud = EstadoTransaccion.objects.get(estado='aprobado')
                if observacion is None:
                    observacion = ""
                if tipoobs == "rp":
                    solicitud.observacion_representante = observacion
                elif tipoobs == "bdg":
                    solicitud.observacion_bodega = observacion
                solicitud.estado_solicitud_id = estado_solicitud.id
                solicitud.fecha_autorizacion = timezone.now()
                solicitud.save()
        else:
            raise Exception('Faltan datos')

    def revision_solicitud(self, tipoobs, observacion):
        if tipoobs is not None:
            with transaction.atomic():
                solicitud = self.object
                if solicitud.estado_solicitud.estado in ['almacenado', 'entregado', 'recibido']:
                    raise Exception("No es posible manipular este registro este registro")
                estado_solicitud = EstadoTransaccion.objects.get(estado='revision')
                if observacion is None:
                    observacion = ""
                if tipoobs == "rp":
                    solicitud.observacion_representante = observacion
                elif tipoobs == "bdg":
                    solicitud.observacion_bodega = observacion
                solicitud.estado_solicitud_id = estado_solicitud.id
                solicitud.save()
        else:
            raise Exception('Faltan datos')

    def entregar_solicitud(self, detalle_solicitud, observacion_solicitud):
        if detalle_solicitud is not None and observacion_solicitud is not None:
            with transaction.atomic():
                detalle_solicitud = json.loads(detalle_solicitud)
                solicitud = self.object
                tipo_movimiento_del = TipoMovimientoInventario.objects.get(nombre='delete')
                tipo_movimiento_add = TipoMovimientoInventario.objects.get(nombre='add')
                estado_solicitud = EstadoTransaccion.objects.get(estado='entregado')
                solicitud.estado_solicitud_id = estado_solicitud.id
                solicitud.observacion_bodega = observacion_solicitud
                solicitud.save()
                for i in solicitud.solicituddetalle_set.all():
                    # actualiza la cantidad a entregar
                    for ds_new in detalle_solicitud:
                        if ds_new['id'] == i.id:
                            i.cantidad_entregada = float(ds_new['cant_ent'])
                            break
                    i.save()
                    # verificar si existe cupo para entregar la sustancia
                    cupo_consumido = i.sustancia.get_cupo_consumido(timezone.now().year)
                    cupo_autorizado = float(i.sustancia.cupo_autorizado)
                    if cupo_consumido + float(i.cantidad_entregada) > cupo_autorizado:
                        raise PermissionDenied(
                            'La sustancia {} sobrepasa el cupo permitido, verifique'.format(
                                i.sustancia.nombre)
                        )
                    # disminuye stock en bodega
                    stockbdg = Stock.objects.get(sustancia_id=i.sustancia.id,
                                                 bodega_id=i.solicitud.bodega.id)
                    stockbdg.cantidad = float(stockbdg.cantidad) - i.cantidad_entregada
                    stockbdg.save()

                    # movimiento de inventario delete de bodega
                    inv = Inventario()
                    inv.solicitud_detalle_id = i.id
                    inv.cantidad_movimiento = i.cantidad_entregada
                    inv.tipo_movimiento_id = tipo_movimiento_del.id
                    inv.save()

                    # Aumenta el stock de el laboratorio
                    stocklab = Stock.objects.get(laboratorio_id=i.solicitud.laboratorio.id,
                                                 sustancia_id=i.sustancia.id)
                    stocklab.cantidad = float(stocklab.cantidad) + i.cantidad_entregada
                    stocklab.save()

                    # movimiento de inventario addsustancialab en el laboratorio
                    invlab = Inventario()
                    invlab.solicitud_detalle_id = i.id
                    invlab.cantidad_movimiento = i.cantidad_entregada
                    invlab.tipo_movimiento_id = tipo_movimiento_add.id
                    invlab.save()
        else:
            raise Exception("Faltan datos")

    def search_detalle(self):
        data = []
        for i in self.object.solicituddetalle_set.all():
            data.append({
                'id': i.id,
                'sustancia': i.sustancia.nombre,
                'cant_bdg': float(i.sustancia.stock_set.get(bodega_id=i.solicitud.bodega.id).cantidad),
                'cant_sol': float(i.cantidad_solicitada),
                'cant_ent': float(i.cantidad_entregada),
                'cant_con': float(i.cantidad_consumida)
            })
        return data
