from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView

from app.settings import LOGIN_REDIRECT_URL
from core.base.mixins import ValidatePermissionRequiredMixin
from core.representantetecnico.models import Inventario


class MovimientosInventarioListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    permission_required = ('representantetecnico.view_inventario',)
    model = Inventario
    template_name = "movimientosinventario/list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Movimientos inventario"
        context['icontitle'] = "store-alt"
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
                    id_data = request.GET.get('id')
                    if type_data == 'lab':
                        query = Inventario.objects.filter(stock__bodega=None)
                    else:
                        query = Inventario.objects.filter(stock__bodega=None)
                    for i in Inventario.objects.filter(stock__bodega=None):
                        item = {'id': i.id, 'sustancia': i.stock.sustancia.nombre, 'cantidad': '', 'mes': '',
                                'year': '', 'lugar': '', 'nom_lug': '', 'un_med': ''}

                        data.append(item)
                    return JsonResponse(data, safe=False)
        except Exception as e:
            data['error'] = str(e)
        return super().get(request, *args, **kwargs)
