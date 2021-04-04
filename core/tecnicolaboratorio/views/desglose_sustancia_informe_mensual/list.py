from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views.generic import ListView

from core.base.mixins import ValidatePermissionRequiredMixin
from core.representantetecnico.models import DesgloseInfomeMensualDetalle


class DesgloseSustanciaInformeMensualListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    permission_required = ('representantetecnico.view_informesmensuales',)
    model = DesgloseInfomeMensualDetalle
    template_name = "desglosesustanciainformemensual/list.html"

    def get(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.GET.get('action')
            if action is not None:
                if action == 'search_desglose_sustancia':
                    data = []
                    detalle_informe_id = int(request.GET.get('detalle_informe_id'))
                    for i in DesgloseInfomeMensualDetalle.objects.filter(informe_mensual_detalle_id=detalle_informe_id):
                        item = {'id': i.id, 'solicitud': "No asignado", 'cantidad_solicitada': 0,
                                'cantidad_consumida_total': 0, 'cantidad_consumida': i.cantidad,
                                'responsable_actividad': "No asignado", 'documento': i.get_documento()}
                        if i.solicitud_detalle is not None:
                            item['solicitud'] = "{} {}".format(i.solicitud_detalle.solicitud.codigo_solicitud,
                                                               i.solicitud_detalle.solicitud.nombre_actividad)
                            item['cantidad_solicitada'] = i.solicitud_detalle.cantidad_solicitada
                            item['cantidad_consumida_total'] = i.solicitud_detalle.cantidad_consumida
                            item['responsable_actividad'] = "{} {}".format(
                                i.solicitud_detalle.solicitud.responsable_actividad.nombre,
                                i.solicitud_detalle.solicitud.responsable_actividad.apellido)
                        data.append(item)
                    return JsonResponse(data, safe=False)
        except Exception as e:
            data['error'] = str(e)
        return super().get(request, *args, **kwargs)
