from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView

from app.settings import LOGIN_REDIRECT_URL
from core.base.mixins import ValidatePermissionRequiredMixin
from core.representantetecnico.models import Inventario, Mes, Sustancia


class EstadoMensualListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    permission_required = ('representantetecnico.view_inventario',)
    model = Inventario
    template_name = "movimientosinventario/estadomensual.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Estado mensual de sustancias"
        context['icontitle'] = "store-alt"
        context['years_disp'] = Inventario.get_years_disp_inv()
        context['meses'] = Mes.objects.all()
        context['urls'] = [
            {"uridj": LOGIN_REDIRECT_URL, "uriname": "Home"},
            {"uridj": reverse_lazy('rp:sustancias'), "uriname": "Inventario"},
            {"uridj": reverse_lazy('rp:estadomensual'), "uriname": "Estados mensuales"}
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
                    if type_data == 'lab_month':
                        data_res = Inventario.get_data_inventario_mov(mes, year, request.user.id, 0)
                    elif type_data == 'bdg_month':
                        data_res = Inventario.get_data_inventario_mov(mes, year, 0, request.user.id)
                    else:
                        data_res = Inventario.get_data_inventario_mov(mes, year, 0, 0)
                    data = data_res
                    return JsonResponse(data, safe=False)
        except Exception as e:
            data['error'] = str(e)
        return super().get(request, *args, **kwargs)
