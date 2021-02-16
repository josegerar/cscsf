from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView

from core.base.mixins import ValidatePermissionRequiredMixin
from core.bodega.models import Inventario


class MovimientosInventarioListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    permission_required = ('bodega.view_inventario',)
    model = Inventario
    template_name = "movimientosinventario/list.html"

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['urls'] = [
            {"uridj": reverse_lazy('dashboard'), "uriname": "Home"},
            {"uridj": reverse_lazy('rp:inventario'), "uriname": "Inventario"},
            {"uridj": reverse_lazy('rp:movimientoinventario'), "uriname": "Movimientos"}
        ]
        context['usertitle'] = "Representante Técnico"
        context['title'] = "Movimientos inventario"
        return context

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Inventario.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data["error"] = str(e)
        return JsonResponse(data, safe=False)
