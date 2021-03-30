from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView

from app.settings import LOGIN_REDIRECT_URL
from core.base.mixins import ValidatePermissionRequiredMixin
from core.bodega.models import Sustancia, Stock


class SustanciaListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    permission_required = ('bodega.view_sustancia',)
    model = Sustancia
    template_name = "sustancia/list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usertitle'] = "Representante Técnico"
        context['title'] = "Sustancias registradas"
        context['icontitle'] = "store-alt"
        context['create_url'] = reverse_lazy('rp:registrosustancias')
        context['urls'] = [
            {"uridj": LOGIN_REDIRECT_URL, "uriname": "Home"},
            {"uridj": reverse_lazy('rp:sustancias'), "uriname": "Sustancias"}
        ]
        return context

    def get(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.GET.get('action')
            if action is not None:
                if action == 'search_substance':
                    data = []
                    substances = Sustancia.objects.filter(nombre__icontains=request.GET['term'])[0:10]
                    for i in substances:
                        substance = i.toJSON(view_stock=True)
                        substance['value'] = i.nombre
                        data.append(substance)
                    return JsonResponse(data, safe=False)
                elif action == 'search_substance_lab':
                    data = []
                    code_lab = request.GET.get('code_lab')
                    if code_lab is not None:
                        for stock in Stock.objects.filter(laboratorio_id=code_lab)[0:10]:
                            if stock.sustancia is not None and stock.sustancia.unidad_medida is not None:
                                data.append({
                                    'id': stock.id,
                                    'value': stock.sustancia.nombre,
                                    'sustancia_id': stock.sustancia.id,
                                    'unidad_medida': stock.sustancia.unidad_medida.nombre,
                                    'cantidad_lab': stock.cantidad
                                })
                    return JsonResponse(data, safe=False)
        except Exception as e:
            data['error'] = str(e)
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Sustancia.objects.all():
                    data.append(i.toJSON(view_stock=True))
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data["error"] = str(e)
        return JsonResponse(data, safe=False)
