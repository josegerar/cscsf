from django.contrib import messages
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
        try:
            action = request.GET.get('action')
            if action is not None:
                if action == 'searchdata':
                    mes = request.GET.get('mes')
                    year = request.GET.get('year')
                    sustancia = request.GET.get('sus_id')
                    data = self.search_data(request.user, sustancia, year, mes)
                    return JsonResponse(data, safe=False)
        except Exception as e:
            messages.error(request, str(e))
        return super().get(request, *args, **kwargs)

    def search_data(self, user, sustancia, year, mes):
        if user.is_laboratory_worker:
            return Inventario.get_mov_inv_tl(user.id, sustancia, year, mes)
        elif user.is_grocer:
            return Inventario.get_mov_inv_bdg(user.id, sustancia, year, mes)
        else:
            return Inventario.get_mov_inv_rt(sustancia, year, mes)
