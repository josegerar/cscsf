from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils import timezone
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
                        item = {
                            'id': i.id,
                            'nombre': i.nombre,
                            'descripcion': i.descripcion,
                            'cupo_autorizado': i.cupo_autorizado,
                            'unidad_medida': i.unidad_medida.nombre,
                            'is_del': True
                        }
                        if i.stock_set.all().exists():
                            item['is_del'] = False
                        data.append(item)
                    return JsonResponse(data, safe=False)
                elif action == 'search_sus_compra':
                    data = []
                    code_bod = request.GET.get('code_bod')
                    for i in Stock.objects.filter(sustancia__nombre__icontains=request.GET['term'], bodega_id=code_bod)[
                             0:10]:
                        item = {'id': i.id, 'cupo_autorizado': float(i.sustancia.cupo_autorizado),
                                'value': i.sustancia.nombre, 'unidad_medida': i.sustancia.unidad_medida.nombre,
                                'cantidad_bodega': float(i.cantidad),
                                'cupo_consumido': i.sustancia.get_cupo_consumido(timezone.now().year)}
                        data.append(item)
                    return JsonResponse(data, safe=False)
                elif action == 'search_sus_bod':
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
                    elif type == 'bdg':
                        query = Stock.objects.filter(bodega__responsable_id=request.user.id, sustancia_id=id_s)
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
                elif action == 'list_desgl_blank':
                    data = []
                    for i in Bodega.objects.all().order_by('nombre'):
                        data.append({'id': i.id, 'nombre': i.nombre, 'tipo': 'bodega', 'cantidad_ingreso': 0.0000})
                    for i in Laboratorio.objects.all().order_by('nombre'):
                        data.append({'id': i.id, 'nombre': i.nombre, 'tipo': 'laboratorio', 'cantidad_ingreso': 0.0000})
                    return JsonResponse(data, safe=False)
                elif action == 'list_desglose':
                    data = []
                    sus_id = request.GET.get('sus_id')
                    for i in Stock.objects.filter(sustancia_id=sus_id, laboratorio=None).order_by(
                            "bodega__nombre"):
                        data.append({'id': i.id, 'nombre': i.bodega.nombre, 'tipo': 'bodega',
                                     'cantidad_ingreso': float(i.cantidad)})
                    for i in Stock.objects.filter(sustancia_id=sus_id, bodega=None).order_by(
                            "laboratorio__nombre"):
                        data.append({'id': i.id, 'nombre': i.laboratorio.nombre, 'tipo': 'laboratorio',
                                     'cantidad_ingreso': float(i.cantidad)})
                    for i in Bodega.objects.exclude(stock__sustancia_id=sus_id).order_by('nombre'):
                        data.append({'id': -1, 'id_lugar': i.id, 'nombre': i.nombre, 'tipo': 'bodega',
                                     'cantidad_ingreso': 0.0000})
                    for i in Laboratorio.objects.exclude(stock__sustancia_id=sus_id).order_by('nombre'):
                        data.append({'id': -1, 'id_lugar': i.id, 'nombre': i.nombre, 'tipo': 'laboratorio',
                                     'cantidad_ingreso': 0.0000})
                    return JsonResponse(data, safe=False)
        except Exception as e:
            data['error'] = str(e)
        return super().get(request, *args, **kwargs)
