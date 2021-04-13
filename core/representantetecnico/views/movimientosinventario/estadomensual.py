from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView

from app.settings import LOGIN_REDIRECT_URL
from core.base.mixins import ValidatePermissionRequiredMixin
from core.representantetecnico.models import Inventario, Mes


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
                    mes = request.GET.get('mes')
                    year = request.GET.get('year')
                    data = self.search_data(request.user, mes, year)
                    return JsonResponse(data, safe=False)
        except Exception as e:
            data['error'] = str(e)
        return super().get(request, *args, **kwargs)

    def search_data(self, user, mes, year):
        if user.is_laboratory_worker:
            return Inventario.get_data_inventario_mov(mes, year, user.id, 0)
        elif user.is_grocer:
            return Inventario.get_data_inventario_mov(mes, year, 0, user.id)
        else:
            return Inventario.get_data_inventario_mov(mes, year, 0, 0)
