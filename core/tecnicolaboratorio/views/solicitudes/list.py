from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView

from app.settings import LOGIN_REDIRECT_URL
from core.base.mixins import ValidatePermissionRequiredMixin
from core.bodega.models import TipoMovimientoInventario, Stock, Inventario
from core.representantetecnico.models import Solicitud, EstadoTransaccion, SolicitudDetalle


class SolicitudListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    permission_required = ('representantetecnico.view_solicitud',)
    model = Solicitud
    template_name = "solicitud/list.html"

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST.get('action')
            if action is not None:
                if action == 'searchdata':
                    data = []
                    for i in Solicitud.objects.all():
                        data.append(i.toJSON())
                elif action == 'revisionSolicitud':
                    idsolicitud = request.POST.get('id')
                    if idsolicitud is not None:
                        with transaction.atomic():
                            solicitud = Solicitud.objects.get(id=idsolicitud)
                            if solicitud is not None:
                                estado_solicitud = EstadoTransaccion.objects.get(estado='revision')
                                if estado_solicitud is not None:
                                    observacion = request.POST.get('observacion')
                                    if observacion is None:
                                        observacion = ""
                                    solicitud.observacion = observacion
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
                    if idsolicitud is not None:
                        with transaction.atomic():
                            solicitud = Solicitud.objects.get(id=idsolicitud)
                            if solicitud is not None:
                                estado_solicitud = EstadoTransaccion.objects.get(estado='aprobado')
                                if estado_solicitud is not None:
                                    solicitud.estado_solicitud_id = estado_solicitud.id
                                    solicitud.save()
                                else:
                                    data['error'] = 'ha ocurrido un error'
                            else:
                                data['error'] = 'ha ocurrido un error'
                elif action == 'entregarSustancias':
                    idsolicitud = request.POST.get('id_solicitud')
                    if idsolicitud is not None:
                        with transaction.atomic():
                            solicitud = Solicitud.objects.get(id=idsolicitud)
                            tipo_movimiento_del = TipoMovimientoInventario.objects.get(nombre='delete')
                            tipo_movimiento_add = TipoMovimientoInventario.objects.get(nombre='addsustancialab')
                            if tipo_movimiento_del is not None:
                                estado_solicitud = EstadoTransaccion.objects.get(estado='entregado')
                                if estado_solicitud is not None:
                                    solicitud.estado_solicitud_id = estado_solicitud.id
                                    solicitud.save()
                                    if solicitud is not None:
                                        detallesustancia = SolicitudDetalle.objects.filter(solicitud_id=solicitud.id)
                                        for i in detallesustancia:
                                            # verificar si existe cupo para entregar la sustancia
                                            cupo_consumido = i.stock.sustancia.get_cupo_consumido()
                                            cupo_autorizado = float(i.stock.sustancia.cupo_autorizado)
                                            if cupo_consumido + float(i.cantidad) > cupo_autorizado:
                                                raise PermissionDenied(
                                                    'La sustancia {} sobrepasa el cupo permitido, verifique'.format(
                                                        i.stock.sustancia.nombre)
                                                )
                                            else:
                                                # disminuye stock en bodega
                                                stockbdg = Stock.objects.get(id=i.stock_id)
                                                stockbdg.cantidad = stockbdg.cantidad - i.cantidad
                                                stockbdg.save()

                                                # movimiento de inventario delete de bodega
                                                inv = Inventario()
                                                inv.stock_id = i.stock_id
                                                inv.cantidad_movimiento = i.cantidad
                                                inv.tipo_movimiento_id = tipo_movimiento_del.id
                                                inv.save()

                                                # Aumenta el stock de el laboratorio
                                                stocklab = Stock.objects.get(laboratorio_id=solicitud.laboratorio.id,
                                                                             sustancia_id=i.stock.sustancia_id)
                                                stocklab.cantidad = stocklab.cantidad + i.cantidad
                                                stocklab.save()

                                                # movimiento de inventario addsustancialab en el laboratorio
                                                invlab = Inventario()
                                                invlab.stock_id = i.stock_id
                                                invlab.cantidad_movimiento = i.cantidad
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
                else:
                    data['error'] = 'Ha ocurrido un error'
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data["error"] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usertitle'] = "Representante Técnico"
        context['title'] = "Solicitudes registradas"
        context['icontitle'] = "store-alt"
        context['create_url'] = reverse_lazy('tl:registrosolicitud')
        context['urls'] = [
            {"uridj": LOGIN_REDIRECT_URL, "uriname": "Home"},
            {"uridj": reverse_lazy('tl:solicitudes'), "uriname": "Solicitudes"}
        ]
        return context
