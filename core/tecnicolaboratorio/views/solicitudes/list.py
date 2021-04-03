import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView

from app.settings import LOGIN_REDIRECT_URL
from core.base.mixins import ValidatePermissionRequiredMixin
from core.representantetecnico.models import Solicitud, EstadoTransaccion, SolicitudDetalle, TipoMovimientoInventario, \
    Inventario, Stock
from core.tecnicolaboratorio.models import Laboratorio


class SolicitudListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    permission_required = ('representantetecnico.view_solicitud',)
    model = Solicitud
    template_name = "solicitud/list.html"

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST.get('action')
            if action is not None:
                if action == 'revisionSolicitud':
                    idsolicitud = request.POST.get('id')
                    tipoobs = request.POST.get("tipoobs")
                    if idsolicitud is not None and tipoobs is not None:
                        with transaction.atomic():
                            solicitud = Solicitud.objects.get(id=idsolicitud)
                            if solicitud is not None:
                                estado_solicitud = EstadoTransaccion.objects.get(estado='revision')
                                if estado_solicitud is not None:
                                    observacion = request.POST.get('observacion')
                                    if observacion is None:
                                        observacion = ""
                                    if tipoobs == "rp":
                                        solicitud.observacion_representante = observacion
                                    elif tipoobs == "bdg":
                                        solicitud.observacion_bodega = observacion
                                    solicitud.estado_solicitud_id = estado_solicitud.id
                                    solicitud.save()
                                else:
                                    data['error'] = 'ha ocurrido un error'
                            else:
                                data['error'] = 'ha ocurrido un error'
                    else:
                        data['error'] = 'ha ocurrido un error'
                elif action == 'aprobarSolicitud':
                    idsolicitud = request.POST.get('id_solicitud')
                    tipoobs = request.POST.get("tipoobs")
                    if idsolicitud is not None and tipoobs is not None:
                        with transaction.atomic():
                            solicitud = Solicitud.objects.get(id=idsolicitud)
                            if solicitud is not None:
                                estado_solicitud = EstadoTransaccion.objects.get(estado='aprobado')
                                if estado_solicitud is not None:
                                    observacion = request.POST.get('observacion')
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
                                    data['error'] = 'ha ocurrido un error'
                            else:
                                data['error'] = 'ha ocurrido un error'
                elif action == 'entregarSolicitud':
                    idsolicitud = request.POST.get('id')
                    detalle_solicitud = request.POST.get('detalles')
                    observacion_solicitud = request.POST.get('observacion')
                    if idsolicitud is not None and detalle_solicitud is not None and observacion_solicitud is not None:
                        with transaction.atomic():
                            detalle_solicitud = json.loads(detalle_solicitud)
                            solicitud = Solicitud.objects.get(id=idsolicitud)
                            tipo_movimiento_del = TipoMovimientoInventario.objects.get(nombre='delete')
                            tipo_movimiento_add = TipoMovimientoInventario.objects.get(nombre='addsustancialab')
                            if tipo_movimiento_del is not None and tipo_movimiento_add is not None:
                                estado_solicitud = EstadoTransaccion.objects.get(estado='entregado')
                                if estado_solicitud is not None:
                                    solicitud.estado_solicitud_id = estado_solicitud.id
                                    solicitud.observacion_bodega = observacion_solicitud
                                    solicitud.save()
                                    if solicitud is not None:
                                        detallesolicitud = SolicitudDetalle.objects.filter(solicitud_id=solicitud.id)
                                        for i in detallesolicitud:
                                            # actualiza la cantidad a entregar
                                            for ds_new in detalle_solicitud:
                                                if ds_new['id'] == i.id:
                                                    i.cantidad_entregada = float(ds_new['cantidad_entrega'])
                                                    break
                                            i.save()
                                            # verificar si existe cupo para entregar la sustancia
                                            cupo_consumido = i.stock.sustancia.get_cupo_consumido()
                                            cupo_autorizado = float(i.stock.sustancia.cupo_autorizado)
                                            if cupo_consumido + float(i.cantidad_entregada) > cupo_autorizado:
                                                raise PermissionDenied(
                                                    'La sustancia {} sobrepasa el cupo permitido, verifique'.format(
                                                        i.stock.sustancia.nombre)
                                                )
                                            else:
                                                # disminuye stock en bodega
                                                stockbdg = Stock.objects.get(id=i.stock_id)
                                                stockbdg.cantidad = float(stockbdg.cantidad) - i.cantidad_entregada
                                                stockbdg.save()

                                                # movimiento de inventario delete de bodega
                                                inv = Inventario()
                                                inv.stock_id = i.stock_id
                                                inv.cantidad_movimiento = i.cantidad_entregada
                                                inv.tipo_movimiento_id = tipo_movimiento_del.id
                                                inv.save()

                                                # Aumenta el stock de el laboratorio
                                                stocklab = Stock.objects.get(laboratorio_id=solicitud.laboratorio.id,
                                                                             sustancia_id=i.stock.sustancia_id)
                                                stocklab.cantidad = float(stocklab.cantidad) + i.cantidad_entregada
                                                stocklab.save()

                                                # movimiento de inventario addsustancialab en el laboratorio
                                                invlab = Inventario()
                                                invlab.stock_id = i.stock_id
                                                invlab.cantidad_movimiento = i.cantidad_entregada
                                                invlab.tipo_movimiento_id = tipo_movimiento_add.id
                                                invlab.save()
                                    else:
                                        raise Exception(
                                            'ha ocurrido un error al intentar confirmar la compra'
                                        )
                                else:
                                    data['error'] = 'ha ocurrido un error al intentar confirmar la compra'
                            else:
                                data['error'] = 'ha ocurrido un error al intentar confirmar la compra'
                elif action == 'recibirSolicitud':
                    idsolicitud = request.POST.get('id')
                    if idsolicitud is not None:
                        with transaction.atomic():
                            solicitud = Solicitud.objects.get(id=idsolicitud)
                            if solicitud is not None:
                                estado_solicitud = EstadoTransaccion.objects.get(estado='recibido')
                                if estado_solicitud is not None:
                                    solicitud.estado_solicitud_id = estado_solicitud.id
                                    solicitud.save()
                                else:
                                    data['error'] = 'ha ocurrido un error'
                            else:
                                data['error'] = 'ha ocurrido un error'
                else:
                    data['error'] = 'Ha ocurrido un error'
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data["error"] = str(e)
        return JsonResponse(data, safe=False)

    def get(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.GET.get('action')
            if action is not None:
                if action == 'search_solicitudes_recibidas':
                    data = []
                    sustancia_id = int(request.GET.get('sustancia_id'))
                    lab_id = int(request.GET.get('lab_id'))
                    det_inf = int(request.GET.get('det_inf'))
                    estado_solicitud = EstadoTransaccion.objects.get(estado="recibido")
                    for i in SolicitudDetalle.objects.filter(stock__sustancia_id=sustancia_id,
                                                             solicitud__laboratorio_id=lab_id,
                                                             solicitud__solicitante_id=request.user.id,
                                                             solicitud__estado_solicitud_id=estado_solicitud.id) \
                            .exclude(desgloseinfomemensualdetalle__informe_mensual_detalle_id=det_inf):
                        item = {'id': i.id, 'cantidad_solicitada': i.cantidad_solicitada,
                                'cantidad_consumida': i.cantidad_consumida,
                                'text': "{} {}".format(i.solicitud.codigo_solicitud, i.solicitud.nombre_actividad),
                                'consumidor': "{} {}".format(i.solicitud.responsable_actividad.nombre,
                                                             i.solicitud.responsable_actividad.apellido)}
                        data.append(item)
                    return JsonResponse(data, safe=False)
                elif action == 'searchdata':
                    data = []
                    type_data = request.GET.get('type')
                    id_data = request.GET.get('id')
                    if type_data == 'lab':
                        query = Solicitud.objects.all().filter(laboratorio_id=id_data)
                    elif type_data == 'est':
                        query = Solicitud.objects.all().filter(estado_solicitud_id=id_data)
                    else:
                        query = Solicitud.objects.all()
                    for i in query:
                        item = {
                            'id': i.id,
                            'laboratorio': i.laboratorio.nombre,
                            'nombre_actividad': i.nombre_actividad,
                            'documento': i.get_doc_solicitud(),
                            'fecha_autorizacion': i.get_fecha_autorizacion(),
                            'estado': i.estado_solicitud.estado,
                            'obs_bd': i.observacion_bodega,
                            'obs_rp': i.observacion_representante
                        }
                        data.append(item)
                    return JsonResponse(data, safe=False)
                elif action == 'search_detalle':
                    data = []
                    id_sl = request.GET.get('id_sl')
                    for i in SolicitudDetalle.objects.filter(solicitud_id=id_sl):
                        data.append({
                            'sustancia': i.stock.sustancia.nombre,
                            'cant_sol': i.cantidad_solicitada,
                            'cant_ent': i.cantidad_entregada,
                            'cant_con': i.cantidad_consumida
                        })
                    return JsonResponse(data, safe=False)
        except Exception as e:
            data['error'] = str(e)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Solicitudes registradas"
        context['icontitle'] = "store-alt"
        context['laboratorios'] = Laboratorio.objects.all()
        context['estados'] = EstadoTransaccion.objects.all()
        context['create_url'] = reverse_lazy('tl:registrosolicitud')
        context['urls'] = [
            {"uridj": LOGIN_REDIRECT_URL, "uriname": "Home"},
            {"uridj": reverse_lazy('tl:solicitudes'), "uriname": "Solicitudes"}
        ]
        return context
