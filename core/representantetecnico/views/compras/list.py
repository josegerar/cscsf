from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView

from app.settings import LOGIN_REDIRECT_URL
from core.base.mixins import ValidatePermissionRequiredMixin
from core.bodega.models import TipoMovimientoInventario, Inventario, Stock
from core.representantetecnico.models import ComprasPublicas, Laboratorio, ComprasPublicasDetalle, EstadoTransaccion, \
    Solicitud


class ComprasListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    permission_required = ('representantetecnico.view_compraspublicas',)
    model = ComprasPublicas
    template_name = "compras/list.html"

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in ComprasPublicas.objects.all():
                    data.append(i.toJSON())
            elif action == 'revisionCompra':
                idcompra = request.POST.get('id_compra')
                if idcompra is not None:
                    with transaction.atomic():
                        comprasPublicas = ComprasPublicas.objects.get(id=idcompra)
                        if comprasPublicas is not None:
                            compras_estado = EstadoTransaccion.objects.get(estado='revision')
                            if compras_estado is not None:
                                comprasPublicas.estado_compra_id = compras_estado.id
                                comprasPublicas.save()
                            else:
                                data['error'] = 'ha ocurrido un error'
                        else:
                            data['error'] = 'ha ocurrido un error'
                else:
                    data['error'] = 'ha ocurrido un error'
            elif action == 'confirmarCompra':
                idcompra = request.POST.get('id_compra')
                if idcompra is not None:
                    with transaction.atomic():
                        comprasPublicas = ComprasPublicas.objects.get(id=idcompra)
                        tipo_movimiento = TipoMovimientoInventario.objects.get(nombre='add')
                        if tipo_movimiento is not None:
                            compras_estado = EstadoTransaccion.objects.get(estado='almacenado')
                            if compras_estado is not None:
                                comprasPublicas.estado_compra_id = compras_estado.id
                                comprasPublicas.save()
                                if comprasPublicas is not None:
                                    detallecompra = ComprasPublicasDetalle.objects.filter(compra_id=comprasPublicas.id)
                                    for i in detallecompra:
                                        stock = Stock.objects.get(id=i.stock_id)
                                        stock.cantidad = stock.cantidad + i.cantidad
                                        stock.save()

                                        inv = Inventario()
                                        inv.stock_id = i.stock_id
                                        inv.cantidad_movimiento = i.cantidad
                                        inv.tipo_movimiento_id = tipo_movimiento.id
                                        inv.save()
                                else:
                                    data['error'] = 'ha ocurrido un error al intentar confirmar la compra'
                            else:
                                data['error'] = 'ha ocurrido un error al intentar confirmar la compra'
                        else:
                            data['error'] = 'ha ocurrido un error al intentar confirmar la compra'
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data["error"] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usertitle'] = "Representante Técnico"
        context['title'] = "Compras registradas"
        context['icontitle'] = "store-alt"
        context['laboratorios'] = Laboratorio.objects.all()
        context['create_url'] = reverse_lazy('rp:registrocompras')
        context['urls'] = [
            {"uridj": LOGIN_REDIRECT_URL, "uriname": "Home"},
            {"uridj": reverse_lazy('rp:compras'), "uriname": "Compras"}
        ]
        return context
