from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView

from app.settings import LOGIN_REDIRECT_URL
from core.base.mixins import ValidatePermissionRequiredMixin
from core.bodega.models import Bodega
from core.representantetecnico.models import Sustancia, UnidadMedida, Stock
from core.tecnicolaboratorio.models import Laboratorio


class SustanciaListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    permission_required = ('representantetecnico.view_sustancia',)
    model = Sustancia
    template_name = "sustancia/list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Sustancias registradas"
        context['icontitle'] = "store-alt"
        context['unidades'] = UnidadMedida.objects.all()
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
                if action == 'searchdata':
                    id_s = request.GET.get('id')
                    type = request.GET.get('type')
                    data = []
                    if type == 'un_med':
                        query = Sustancia.objects.filter(unidad_medida_id=id_s)
                    else:
                        query = Sustancia.objects.all()
                    for i in query:
                        data.append({
                            'id': i.id,
                            'nombre': i.nombre,
                            'descripcion': i.descripcion,
                            'cupo_autorizado': i.cupo_autorizado,
                            'unidad_medida': i.unidad_medida.nombre
                        })
                    return JsonResponse(data, safe=False)
                elif action == 'search_substance':
                    data = []
                    substances = Sustancia.objects.filter(nombre__icontains=request.GET['term'])[0:10]
                    for i in substances:
                        substance = i.toJSON(view_stock=True)
                        substance['value'] = i.nombre
                        data.append(substance)
                    return JsonResponse(data, safe=False)
                elif action == 'search_sus_comp':
                    data = []
                    code_bod = request.GET.get('code_bod')
                    term = request.GET.get('term')
                    for i in Stock.objects.filter(sustancia__nombre__icontains=term, bodega_id=code_bod)[0:10]:
                        item = {'id': i.id, 'cupo_autorizado': i.sustancia.cupo_autorizado, 'value': i.sustancia.nombre,
                                'unidad_medida': i.sustancia.unidad_medida.nombre, 'cantidad_bodega': i.cantidad}
                        data.append(item)
                    return JsonResponse(data, safe=False)
                elif action == 'search_sus_lab':
                    data = []
                    code_lab = request.GET.get('code_lab')
                    if code_lab is not None:
                        for stock in Stock.objects.filter(laboratorio_id=code_lab)[0:10]:
                            if stock.sustancia is not None and stock.sustancia.unidad_medida is not None:
                                data.append({
                                    'id': stock.id,
                                    'value': stock.sustancia.nombre,
                                    'unidad_medida': stock.sustancia.unidad_medida.nombre,
                                    'cantidad_lab': stock.cantidad
                                })
                    return JsonResponse(data, safe=False)
                elif action == 'search_stock':
                    id_s = request.GET.get('id_s')
                    type = request.GET.get('type')
                    data = []
                    if type == 'lab':
                        query = Stock.objects.filter(laboratorio__responsable_id=request.user.id, sustancia_id=id_s)
                    else:
                        query = Stock.objects.filter(sustancia_id=id_s)
                    for i in query:
                        item = {'id': i.id, 'cantidad': i.cantidad, 'type': '', 'nombre': ''}
                        if i.laboratorio is not None:
                            item['type'] = 'laboratorio'
                            item['nombre'] = i.laboratorio.nombre
                        elif i.bodega is not None:
                            item['type'] = 'bodega'
                            item['nombre'] = i.bodega.nombre
                        data.append(item)
                    return JsonResponse(data, safe=False)
                elif action == 'list_desglose':
                    data = []
                    for i in Bodega.objects.all().order_by('nombre'):
                        item = i.toJSON()
                        item['tipo'] = 'bodega'
                        item['cantidad_ingreso'] = 0.0000
                        data.append(item)
                    for i in Laboratorio.objects.all().order_by('nombre'):
                        item = i.toJSON()
                        item['tipo'] = 'laboratorio'
                        item['cantidad_ingreso'] = 0.0000
                        data.append(item)
                    return JsonResponse(data, safe=False)
        except Exception as e:
            data['error'] = str(e)
        return super().get(request, *args, **kwargs)
