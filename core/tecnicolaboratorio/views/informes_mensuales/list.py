from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView

from app.settings import LOGIN_REDIRECT_URL
from core.base.mixins import ValidatePermissionRequiredMixin
from core.bodega.models import TipoMovimientoInventario, Stock, Inventario
from core.representantetecnico.models import Solicitud, EstadoTransaccion, SolicitudDetalle, InformesMensuales


class InformesMensualesListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    permission_required = ('representantetecnico.view_informesmensuales',)
    model = InformesMensuales
    template_name = "informesmensuales/list.html"

    def get(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.GET.get('action')
            if action is not None:
                if action == 'searchdata':
                    data = []
                    for i in InformesMensuales.objects.all():
                        item = {
                            'id': i.id,
                            'laboratorio': i.laboratorio.nombre,
                            'mes': i.mes.nombre,
                            'year': i.date_creation.year,
                            'is_editable': i.is_editable
                        }
                        data.append(item)
                    return JsonResponse(data, safe=False)
        except Exception as e:
            data['error'] = str(e)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Informes mensuales registrados"
        context['icontitle'] = "store-alt"
        context['create_url'] = reverse_lazy('tl:registroinformesmensuales')
        context['urls'] = [
            {"uridj": LOGIN_REDIRECT_URL, "uriname": "Home"},
            {"uridj": reverse_lazy('tl:informesmensuales'), "uriname": "Informes mesuales"}
        ]
        return context
