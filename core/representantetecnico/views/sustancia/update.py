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
    permission_required = ('bodega.change_sustancia',)
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
                                tipo_movimiento_add = TipoMovimientoInventario.objects.get(nombre='addsustancia')
                                tipo_movimiento_del = TipoMovimientoInventario.objects.get(nombre='delete')
                                sustancia.save()

                                stock_old = Stock.objects.filter(sustancia_id=sustancia.id)

                                for st_old in stock_old:
                                    exits_old = False
                                    for st_new in stock_new:
                                        if st_old.id == st_new['id']:
                                            exits_old = True
                                            break
                                    if exits_old is False:
                                        inv = Inventario()
                                        inv.cantidad_movimiento = st_old.cantidad
                                        inv.tipo_movimiento_id = tipo_movimiento_del.id
                                        inv.save()
                                        st_old.delete()

                                stock_old = Stock.objects.filter(sustancia_id=sustancia.id)

                                for st_new in stock_new:
                                    exits_old = False
                                    item_stock_new = None
                                    for st_old in stock_old:
                                        if st_old.id == st_new['id']:
                                            exits_old = True
                                            item_stock_new = st_old
                                            break
                                    if exits_old is False and item_stock_new is None:
                                        item_stock_new = Stock()

                                    if float(item_stock_new.cantidad) != st_new['cantidad_ingreso']:
                                        inv = Inventario()
                                        inv.stock_id = item_stock_new.id
                                        if item_stock_new.cantidad > st_new['cantidad_ingreso']:
                                            inv.cantidad_movimiento = float(item_stock_new.cantidad) - st_new[
                                                'cantidad_ingreso']
                                            inv.tipo_movimiento_id = tipo_movimiento_del.id
                                        else:
                                            inv.cantidad_movimiento = st_new['cantidad_ingreso'] - float(
                                                item_stock_new.cantidad)
                                            inv.tipo_movimiento_id = tipo_movimiento_add.id
                                        inv.save()

                                        item_stock_new.cantidad = st_new['cantidad_ingreso']
                                        item_stock_new.sustancia_id = sustancia.id
                                        if st_new['tipo'] == 'bodega':
                                            bodega_new = st_new['bodega']
                                            item_stock_new.bodega_id = bodega_new['id']
                                        elif st_new['tipo'] == 'laboratorio':
                                            laboratorio_new = st_new['laboratorio']
                                            item_stock_new.laboratorio_id = laboratorio_new['id']
                                        item_stock_new.save()
                        else:
                            data['error'] = "Ha ocurrido un error"
                    else:
                        data['error'] = "Ha ocurrido un error"
                elif action == 'list_desglose':
                    data = []
                    for i in Stock.objects.filter(sustancia_id=self.object.id, laboratorio=None).order_by(
                            "bodega__nombre"):
                        item = {'id': i.id, 'nombre': i.bodega.nombre, 'tipo': 'bodega',
                                'cantidad_ingreso': float(i.cantidad), 'bodega': i.bodega.toJSON()}
                        data.append(item)
                    for i in Stock.objects.filter(sustancia_id=self.object.id, bodega=None).order_by(
                            "laboratorio__nombre"):
                        item = {'id': i.id, 'nombre': i.laboratorio.nombre, 'tipo': 'laboratorio',
                                'cantidad_ingreso': float(i.cantidad), 'laboratorio': i.laboratorio.toJSON()}
                        data.append(item)
                else:
                    data['error'] = "Ha ocurrido un error"
            else:
                data['error'] = "Ha ocurrido un error"
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)
