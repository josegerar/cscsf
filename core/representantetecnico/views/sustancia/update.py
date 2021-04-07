import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from app.settings import LOGIN_REDIRECT_URL
from core.base.mixins import ValidatePermissionRequiredMixin
from core.representantetecnico.forms.formSustancia import SustanciaForm
from core.representantetecnico.models import TipoMovimientoInventario, Inventario, Sustancia, Stock


class SustanciaUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    permission_required = ('representantetecnico.change_sustancia',)
    model = Sustancia
    form_class = SustanciaForm
    template_name = 'sustancia/create.html'
    success_url = reverse_lazy('rp:sustancias')
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Actualizar sustancia"
        context['icontitle'] = "edit"
        context['url_list'] = self.success_url
        context['action'] = 'edit'
        context['urls'] = [
            {"uridj": LOGIN_REDIRECT_URL, "uriname": "Home"},
            {"uridj": self.success_url, "uriname": "Sustancia"},
            {"uridj": reverse_lazy('rp:actualizacionsustancia'), "uriname": "Edicción"}
        ]
        return context

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST.get('action')
            if action is not None:
                if action == 'edit':
                    form = self.get_form()
                    if form.is_valid():
                        sustancia = form.instance
                        if sustancia is not None:
                            with transaction.atomic():
                                stock_new = json.loads(request.POST['desgloses'])
                                tipo_movimiento_add = TipoMovimientoInventario.objects.get(nombre='add')
                                tipo_movimiento_del = TipoMovimientoInventario.objects.get(nombre='delete')
                                sustancia.save()

                                stock_old = Stock.objects.filter(sustancia_id=sustancia.id)
                                """Actualizar los stock ya agregados"""
                                for st_old in stock_old:
                                    for st_new in stock_new:
                                        if st_old.id == st_new['id']:
                                            if float(st_old.cantidad) != st_new['cantidad_ingreso']:
                                                inv = Inventario()
                                                inv.stock_id = st_old.id
                                                if float(st_old.cantidad) > st_new['cantidad_ingreso']:
                                                    inv.tipo_movimiento_id = tipo_movimiento_del.id
                                                    inv.cantidad_movimiento = float(st_old.cantidad) - st_new['cantidad_ingreso']
                                                if float(st_old.cantidad) < st_new['cantidad_ingreso']:
                                                    inv.tipo_movimiento_id = tipo_movimiento_add.id
                                                    inv.cantidad_movimiento = st_new['cantidad_ingreso'] - float(st_old.cantidad)
                                                stock_old.cantidad = st_new['cantidad_ingreso']
                                                inv.save()
                                                st_old.save()
                                            break
                                """Añadir nuevos stock en caso de que se haya añadido un laboratorio o bodega nuevo"""
                                for st_new in stock_new:
                                    if st_new['id'] == -1:
                                        stock = Stock()
                                        stock.sustancia_id = sustancia.id
                                        if st_new['tipo'] == 'bodega':
                                            stock.bodega_id = st_new['id_lugar']
                                        elif st_new['tipo'] == 'laboratorio':
                                            stock.laboratorio_id = st_new['id_lugar']
                                        stock.cantidad = float(st_new['cantidad_ingreso'])
                                        stock.save()

                                        inv = Inventario()
                                        inv.stock_id = stock.id
                                        inv.cantidad_movimiento = stock.cantidad
                                        inv.tipo_movimiento_id = tipo_movimiento_add.id
                                        inv.save()
                        else:
                            data['error'] = "Ha ocurrido un error"
                    else:
                        data['error'] = form.errors
                else:
                    data['error'] = "Ha ocurrido un error"
            else:
                data['error'] = "Ha ocurrido un error"
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)
