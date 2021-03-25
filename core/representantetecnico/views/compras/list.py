from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView

from app.settings import LOGIN_REDIRECT_URL
from core.base.mixins import ValidatePermissionRequiredMixin
from core.bodega.models import TipoMovimientoInventario, Inventario, Stock
from core.representantetecnico.models import ComprasPublicas, Laboratorio, ComprasPublicasDetalle, EstadoTransaccion


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
                        compras_publicas = ComprasPublicas.objects.get(id=idcompra)
                        if compras_publicas is not None:
                            compras_estado = EstadoTransaccion.objects.get(estado='revision')
                            if compras_estado is not None:
                                compras_publicas.estado_compra_id = compras_estado.id
                                observacion = request.POST.get('observacion')
                                if observacion is None:
                                    observacion = ""
                                compras_publicas.observacion = observacion
                                compras_publicas.save()
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
                        compras_publicas = ComprasPublicas.objects.get(id=idcompra)
                        tipo_movimiento = TipoMovimientoInventario.objects.get(nombre='addcompra')
                        if tipo_movimiento is not None:
                            compras_estado = EstadoTransaccion.objects.get(estado='almacenado')
                            if compras_estado is not None:
                                compras_publicas.estado_compra_id = compras_estado.id
                                compras_publicas.save()
                                if compras_publicas is not None:
                                    detallecompra = ComprasPublicasDetalle.objects.filter(compra_id=compras_publicas.id)
                                    for i in detallecompra:
                                        # verificar si existe cupo para entregar la sustancia
                                        cupo_consumido = i.stock.sustancia.get_cupo_consumido()
                                        cupo_autorizado = float(i.stock.sustancia.cupo_autorizado)
                                        if cupo_consumido + float(i.cantidad) > cupo_autorizado:
                                            raise PermissionDenied(
                                                'La sustancia {} sobrepasa el cupo permitido, verifique'.format(
                                                    i.stock.sustancia.nombre)
                                            )
                                        else:
                                            stock = Stock.objects.get(id=i.stock_id)
                                            stock.cantidad = stock.cantidad + i.cantidad
                                            stock.save()

                                            inv = Inventario()
                                            inv.stock_id = i.stock_id
                                            inv.cantidad_movimiento = i.cantidad
                                            inv.tipo_movimiento_id = tipo_movimiento.id
                                            inv.save()
                                else:
                                    raise Exception(
                                        'ha ocurrido un error al intentar confirmar la compra'
                                    )
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
