from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView

from app.settings import LOGIN_REDIRECT_URL
from core.base.mixins import ValidatePermissionRequiredMixin
from core.representantetecnico.models import Inventario, Mes, Sustancia


class MovimientosInventarioListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    permission_required = ('representantetecnico.view_inventario',)
    model = Inventario
    template_name = "movimientosinventario/list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Movimientos inventario"
        context['icontitle'] = "store-alt"
        context['years_disp'] = Inventario.get_years_disp_inv()
        context['sustancias'] = Sustancia.objects.all()
        context['meses'] = Mes.objects.all()
        context['create_url'] = reverse_lazy('rp:registrocompras')
        context['urls'] = [
            {"uridj": LOGIN_REDIRECT_URL, "uriname": "Home"},
            {"uridj": reverse_lazy('rp:sustancias'), "uriname": "Inventario"},
            {"uridj": reverse_lazy('rp:movimientoinventario'), "uriname": "Movimientos"}
        ]
        return context

    def get(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.GET.get('action')
            if action is not None:
                if action == 'searchdata':
                    data = []
                    type_data = request.GET.get('type')
                    mes = request.GET.get('mes')
                    year = request.GET.get('year')
                    sustancia = request.GET.get('sus_id')
                    if type_data == 'lab':
                        data_res = Inventario.get_data_mov_inv(request.user.id, sustancia, year, mes)
                    elif type_data == 'bdg':
                        data_res = Inventario.get_mov_inv_bdg(request.user.id, sustancia, year, mes)
                    else:
                        data_res = Inventario.get_data_mov_inv(0, 0, 0, 0)
                    data = data_res
                    return JsonResponse(data, safe=False)
        except Exception as e:
            data['error'] = str(e)
        return super().get(request, *args, **kwargs)
