import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView

from app.settings import LOGIN_REDIRECT_URL
from core.base.mixins import ValidatePermissionRequiredMixin
from core.bodega.models import Sustancia, Inventario, TipoMovimientoInventario
from core.representantetecnico.forms.formCompra import ComprasForm
from core.representantetecnico.models import ComprasPublicas, ComprasPublicasDetalle


class ComprasCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    # appname.action(add, change, delete, view)_table
    permission_required = (
        'representantetecnico.add_compraspublicas',
        'representantetecnico.add_compraspublicasdetalle',
    )
    model = ComprasPublicas
    form_class = ComprasForm
    template_name = 'compras/create.html'
    success_url = reverse_lazy('rp:compras')
    url_redirect = success_url

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usertitle'] = "Representante Técnico"
        context['title'] = "Registrar compra"
        context['icontitle'] = "plus"
        context['url_list'] = self.success_url
        context['action'] = 'add'
        context['urls'] = [
            {"uridj": LOGIN_REDIRECT_URL, "uriname": "Home"},
            {"uridj": self.success_url, "uriname": "Compras"},
            {"uridj": reverse_lazy('rp:registrocompras'), "uriname": "Registro"}
        ]
        return context

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_substance':
                data = []
                substances = Sustancia.objects.filter(nombre__icontains=request.POST['term'])[0:10]
                for i in substances:
                    substance = i.toJSON()
                    substance['value'] = i.nombre
                    data.append(substance)
            elif action == 'add':
                form = self.get_form()
                if form.is_valid():
                    compra = form.instance
                    if compra is not None:
                        with transaction.atomic():
                            sustancias = json.loads(request.POST['sustancias'])
                            tipo_movimiento = TipoMovimientoInventario.objects.get(nombre='add')
                            compra.save()

                            for i in sustancias:
                                stock_selected = i['stock_selected']

                                det = ComprasPublicasDetalle()
                                det.stock_id = stock_selected['id']
                                det.compra_id = compra.id
                                det.cantidad = float(i['cantidad'])
                                det.save()

                                inv = Inventario()
                                inv.stock_id = det.stock_id
                                inv.cantidad_movimiento = det.cantidad
                                inv.tipo_movimiento_id = tipo_movimiento.id
                                inv.save()
            else:
                data['error'] = 'No ha realizado ninguna accion'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)
