from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView

from app.settings import LOGIN_REDIRECT_URL
from core.base.mixins import ValidatePermissionRequiredMixin
from core.representantetecnico.models import Solicitud, EstadoTransaccion, SolicitudDetalle
from core.tecnicolaboratorio.models import Laboratorio


class SolicitudListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    permission_required = ('representantetecnico.view_solicitud',)
    model = Solicitud
    template_name = "solicitud/list.html"

    def get(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.GET.get('action')
            if action is not None:
                if action == 'search_sol_rec':
                    data = [{'id': '', 'text': '---------'}]
                    id_stock = int(request.GET.get('stock_id'))
                    lab_id = int(request.GET.get('lab_id'))
                    det_inf = int(request.GET.get('det_inf'))
                    estado_solicitud = EstadoTransaccion.objects.get(estado="recibido")
                    for i in SolicitudDetalle.objects.filter(stock_id=id_stock,
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
                        if request.user.is_laboratory_worker:
                            query = Solicitud.objects.all().filter(laboratorio_id=id_data,
                                                                   laboratorio__responsable_id=request.user.id)
                        elif request.user.is_grocer:
                            query = Solicitud.objects.all().filter(laboratorio_id=id_data,
                                                                   bodega__responsable_id=request.user.id)
                        else:
                            query = Solicitud.objects.all().filter(laboratorio_id=id_data)
                    elif type_data == 'est':
                        if request.user.is_grocer:
                            query = Solicitud.objects.all().filter(estado_solicitud_id=id_data,
                                                                   bodega__responsable_id=request.user.id)
                        elif request.user.is_laboratory_worker:
                            query = Solicitud.objects.all().filter(estado_solicitud_id=id_data,
                                                                   laboratorio__responsable_id=request.user.id)
                        else:
                            query = Solicitud.objects.all().filter(estado_solicitud_id=id_data)
                    else:
                        if request.user.is_grocer:
                            query = Solicitud.objects.filter(bodega__responsable_id=request.user.id)
                        elif request.user.is_laboratory_worker:
                            query = Solicitud.objects.filter(laboratorio__responsable_id=request.user.id)
                        else:
                            query = Solicitud.objects.all()
                    for i in query:
                        item = {
                            'id': i.id,
                            'codigo': i.codigo_solicitud,
                            'solicitante': i.solicitante.get_user_info(),
                            'laboratorio': i.laboratorio.nombre,
                            'nombre_actividad': i.nombre_actividad,
                            'fecha_autorizacion': i.get_fecha_autorizacion(),
                            'estado': i.estado_solicitud.estado,
                        }
                        data.append(item)
                    return JsonResponse(data, safe=False)
                elif action == 'search_detalle':
                    data = []
                    id_sl = request.GET.get('id_sl')
                    for i in SolicitudDetalle.objects.filter(solicitud_id=id_sl):
                        data.append({
                            'id': i.id,
                            'sustancia': i.sustancia.nombre,
                            'cant_bdg': float(i.sustancia.stock_set.get(bodega_id=i.solicitud.bodega.id).cantidad),
                            'cant_sol': float(i.cantidad_solicitada),
                            'cant_ent': float(i.cantidad_entregada),
                            'cant_con': float(i.cantidad_consumida)
                        })
                    return JsonResponse(data, safe=False)
                elif action == 'searchdetail':
                    data = []
                    id_sol = request.GET.get('id_sol')
                    for dci in SolicitudDetalle.objects.filter(solicitud_id=id_sol):
                        item = {'id': dci.id, 'cantidad_solicitud': dci.cantidad_solicitada,
                                'bodega_selected': {'id': dci.solicitud.bodega.id, 'text': dci.solicitud.bodega.nombre},
                                'lab_selected': {'id': dci.solicitud.laboratorio.id,
                                                 'text': dci.solicitud.laboratorio.nombre},
                                'sustancia': {'id': dci.sustancia.id, 'cupo_autorizado': dci.sustancia.cupo_autorizado,
                                              'value': dci.sustancia.nombre,
                                              'unidad_medida': dci.sustancia.unidad_medida.nombre,
                                              'cantidad_bodega': dci.sustancia.stock_set.get(
                                                  bodega_id=dci.solicitud.bodega_id).cantidad}}
                        data.append(item)
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
