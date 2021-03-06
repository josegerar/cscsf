import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView

from app.settings import LOGIN_REDIRECT_URL
from core.base.mixins import ValidatePermissionRequiredMixin
from core.representantetecnico.forms.formSustancia import SustanciaForm
from core.representantetecnico.models import TipoMovimientoInventario, Inventario, Sustancia, Stock


class SustanciaCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    permission_required = ('representantetecnico.add_sustancia',)
    model = Sustancia
    form_class = SustanciaForm
    template_name = "sustancia/create.html"
    success_url = reverse_lazy("rp:sustancias")
    url_redirect = success_url

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                if form.is_valid():
                    sustancia = form.instance
                    lugares = json.loads(request.POST['desgloses'])
                    self.crear_sustancia(sustancia, lugares)
                else:
                    data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Registro sustancias"
        context['icontitle'] = "plus"
        context['url_list'] = self.success_url
        context['action'] = 'add'
        context['urls'] = [
            {"uridj": LOGIN_REDIRECT_URL, "uriname": "Home"},
            {"uridj": self.success_url, "uriname": "Sustancias"},
            {"uridj": reverse_lazy('rp:registrosustancias'), "uriname": "Registro"}
        ]
        return context

    def crear_sustancia(self, sustancia, lugares):
        with transaction.atomic():
            tipo_movimiento_add = TipoMovimientoInventario.objects.get(nombre='add')
            sustancia.save()

            for i in lugares:
                stock = Stock()
                stock.sustancia_id = sustancia.id
                if i['tipo'] == 'bodega':
                    stock.bodega_id = i['id']
                elif i['tipo'] == 'laboratorio':
                    stock.laboratorio_id = i['id']
                stock.cantidad = float(i['cantidad_ingreso'])
                stock.save()

                inv = Inventario()
                inv.stock_id = stock.id
                inv.cantidad_movimiento = stock.cantidad
                inv.tipo_movimiento_id = tipo_movimiento_add.id
                inv.save()
