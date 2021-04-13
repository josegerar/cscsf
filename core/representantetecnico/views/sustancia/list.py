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
                    data = self.search_data(type, id_s, request.user)
                    return JsonResponse(data, safe=False)
                elif action == 'search_sus_compra':
                    code_bod = request.GET.get('code_bod')
                    term = request.GET.get('term')
                    data = self.search_sus_compra(code_bod, term)
                    return JsonResponse(data, safe=False)
                elif action == 'search_sus_bod':
                    code_bod = request.GET.get('code_bod')
                    term = request.GET.get('term')
                    data = self.search_sus_bod(code_bod, term)
                    return JsonResponse(data, safe=False)
                elif action == 'search_sus_lab':
                    code_lab = request.GET.get('code_lab')
                    data = self.search_sus_lab(code_lab)
                    return JsonResponse(data, safe=False)
                elif action == 'search_sus_bod_lab':
                    data = []
                    code_lab = request.GET.get('code_lab')
                    code_bod = request.GET.get('code_bod')
                    term = request.GET.get('term')
                    if code_lab is not None and code_bod is not None:
                        data = Sustancia.get_substances_solicitud(code_lab, code_bod, term)
                    return JsonResponse(data, safe=False)
                elif action == 'list_desgl_blank':
                    data = self.list_desgl_blank()
                    return JsonResponse(data, safe=False)
        except Exception as e:
            data['error'] = str(e)
        return super().get(request, *args, **kwargs)

    def search_data(self, type, id_s, user):
        data = []
        if type == 'un_med':
            if user.is_laboratory_worker:
                query = Sustancia.objects.filter(unidad_medida_id=id_s, stock__laboratorio__responsable_id=user.id)
            elif user.is_grocer:
                query = Sustancia.objects.filter(unidad_medida_id=id_s, stock__bodega__responsable_id=user.id)
            else:
                query = Sustancia.objects.filter(unidad_medida_id=id_s)
        else:
            if user.is_laboratory_worker:
                query = Sustancia.objects.filter(stock__laboratorio__responsable_id=user.id)
            elif user.is_grocer:
                query = Sustancia.objects.filter(stock__bodega__responsable_id=user.id)
            else:
                query = Sustancia.objects.all()
        for i in query:
            item = {
                'id': i.id,
                'nombre': i.nombre,
                'cupo_autorizado': i.cupo_autorizado,
                'unidad_medida': i.unidad_medida.nombre,
                'is_del': i.is_del()
            }
            data.append(item)
        return data

    def search_sus_compra(self, code_bod, term):
        data = []
        for i in Stock.objects.filter(sustancia__nombre__icontains=term, bodega_id=code_bod)[
                 0:10]:
            item = {'id': i.id, 'cupo_autorizado': float(i.sustancia.cupo_autorizado),
                    'value': i.sustancia.nombre, 'unidad_medida': i.sustancia.unidad_medida.nombre,
                    'cantidad_bodega': float(i.cantidad),
                    'cupo_consumido': i.sustancia.get_cupo_consumido(timezone.now().year)}
            data.append(item)
        return data

    def search_sus_bod(self, code_bod, term):
        data = []
        for i in Stock.objects.filter(sustancia__nombre__icontains=term, bodega_id=code_bod)[0:10]:
            item = {'id': i.id, 'cupo_autorizado': i.sustancia.cupo_autorizado, 'value': i.sustancia.nombre,
                    'unidad_medida': i.sustancia.unidad_medida.nombre, 'cantidad_bodega': i.cantidad}
            data.append(item)
        return data

    def search_sus_lab(self, code_lab):
        data = []
        for stock in Stock.objects.filter(laboratorio_id=code_lab)[0:10]:
            if stock.sustancia is not None and stock.sustancia.unidad_medida is not None:
                data.append({
                    'id': stock.id,
                    'value': stock.sustancia.nombre,
                    'unidad_medida': stock.sustancia.unidad_medida.nombre,
                    'cantidad_lab': stock.cantidad
                })
        return data

    def list_desgl_blank(self):
        data = []
        for i in Bodega.objects.all().order_by('nombre'):
            data.append({'id': i.id, 'nombre': i.nombre, 'tipo': 'bodega', 'cantidad_ingreso': 0.0000})
        for i in Laboratorio.objects.all().order_by('nombre'):
            data.append({'id': i.id, 'nombre': i.nombre, 'tipo': 'laboratorio', 'cantidad_ingreso': 0.0000})
        return data


