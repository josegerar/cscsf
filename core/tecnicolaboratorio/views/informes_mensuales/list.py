from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView

from app.settings import LOGIN_REDIRECT_URL
from core.base.formaters import format_datetime
from core.base.mixins import ValidatePermissionRequiredMixin
from core.representantetecnico.models import InformesMensuales, InformesMensualesDetalle, Mes


class InformesMensualesListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    permission_required = ('representantetecnico.view_informesmensuales',)
    model = InformesMensuales
    template_name = "informesmensuales/list.html"

    def get(self, request, *args, **kwargs):
        try:
            action = request.GET.get('action')
            if action is not None:
                if action == 'searchdata':
                    type_data = request.GET.get('type')
                    id_data = request.GET.get('id')
                    data = self.search_data(type_data, id_data, request.user)
                    return JsonResponse(data, safe=False)
                elif action == 'informe_detail':
                    informe_id = request.GET.get('informe_id')
                    data = self.get_informe_detail(informe_id)
                    return JsonResponse(data, safe=False)
                elif action == 'search_months_dsp':
                    year = request.GET.get('year')
                    data = self.search_months_dsp(year)
                    return JsonResponse(data, safe=False)
        except Exception as e:
            messages.error(request, str(e))
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Informes mensuales registrados"
        context['icontitle'] = "store-alt"
        context['meses'] = Mes.objects.all()
        context['years'] = InformesMensuales.objects.order_by('year').distinct("year").values('year')
        context['create_url'] = reverse_lazy('tl:registroinformesmensuales')
        context['urls'] = [
            {"uridj": LOGIN_REDIRECT_URL, "uriname": "Home"},
            {"uridj": reverse_lazy('tl:informesmensuales'), "uriname": "Informes mesuales"}
        ]
        return context

    def search_data(self, type_data, id_data, user):
        data = []
        if type_data == 'year':
            if user.is_laboratory_worker:
                query = InformesMensuales.objects.filter(year=id_data, laboratorista_id=user.id)
            else:
                query = InformesMensuales.objects.filter(year=id_data)
        elif type_data == 'mes':
            if user.is_laboratory_worker:
                query = InformesMensuales.objects.filter(mes_id=id_data, laboratorista_id=user.id)
            else:
                query = InformesMensuales.objects.filter(mes_id=id_data)
        else:
            if user.is_laboratory_worker:
                query = InformesMensuales.objects.filter(laboratorista_id=user.id)
            else:
                query = InformesMensuales.objects.all()
        for i in query:
            item = {
                'id': i.id,
                'laboratorio': i.laboratorio.nombre,
                'mes': i.mes.nombre,
                'year': i.year,
                'fecha_creat': format_datetime(i.date_creation),
                'estado': i.estado_informe.estado
            }
            data.append(item)
        return data

    def search_months_dsp(self, year):
        data = []
        for y in Mes.objects.exclude(informesmensuales__year=year):
            data.append({'id': y.id, 'text': y.nombre})
        return data

    def get_informe_detail(self, informe_id):
        data = []
        for i in InformesMensualesDetalle.objects.filter(informe_id=informe_id):
            data.append({
                'id': i.id,
                'laboratorio': {'id': i.stock.laboratorio.id, 'text': i.stock.laboratorio.nombre},
                'stock': {'id': i.stock.id,
                          'nombre': i.stock.sustancia.nombre,
                          'unidad_medida': i.stock.sustancia.unidad_medida.nombre,
                          'cantidad_lab': i.stock.cantidad},
                'cantidad': i.cantidad
            })
        return data
