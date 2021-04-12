from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import TemplateView

from core.base.mixins import ValidatePermissionRequiredMixin
from core.representantetecnico.models import ComprasPublicas, EstadoTransaccion, TipoMovimientoInventario, Stock, \
    Inventario


class ComprasView(LoginRequiredMixin, ValidatePermissionRequiredMixin, TemplateView):
    permission_required = ('representantetecnico.view_compraspublicas',)
    template_name = 'compras/view.html'
    url_redirect = reverse_lazy('rp:compras')

    def dispatch(self, request, *args, **kwargs):
        try:
            self.object = ComprasPublicas.objects.get(pk=kwargs['pk'])
            return super().dispatch(request, *args, **kwargs)
        except Exception as e:
            messages.error(request, str(e))
        return HttpResponseRedirect(self.url_redirect)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url_list'] = self.url_redirect
        context['icontitle'] = 'eye'
        context['title'] = '{} {}'.format("Compra", self.object.id)
        return context

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'revisionCompra':
                observacion = request.POST.get('observacion')
                if self.object.bodega.responsable_id != request.user.id:
                    raise Exception(
                        "No puede realizar acciones sobre esta compra, no tiene esta bodega asignada")
                self.revision_compra(observacion)
            elif action == 'confirmarCompra':
                observacion = request.POST.get('observacion')
                if self.object.bodega.responsable_id != request.user.id:
                    raise Exception(
                        "No puede realizar acciones sobre esta compra, no tiene esta bodega asignada")
                self.confirmar_compra(observacion)
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data["error"] = str(e)
        return JsonResponse(data, safe=False)

    def confirmar_compra(self, observacion):
        with transaction.atomic():
            compras_publicas = self.object
            if compras_publicas.estado_compra.estado == 'almacenado':
                raise Exception(
                    "Compra ya almacenada en stock, no se puede actualizar"
                )
            tipo_movimiento = TipoMovimientoInventario.objects.get(nombre='add')
            compras_estado = EstadoTransaccion.objects.get(estado='almacenado')
            compras_publicas.estado_compra_id = compras_estado.id
            if observacion is None:
                observacion = ""
            compras_publicas.observacion = observacion
            compras_publicas.save()
            for i in compras_publicas.compraspublicasdetalle_set.all():
                # verificar si existe cupo para entregar la sustancia
                cupo_consumido = i.stock.sustancia.get_cupo_consumido(timezone.now().year)
                cupo_autorizado = float(i.stock.sustancia.cupo_autorizado)
                if cupo_consumido + float(i.cantidad) > cupo_autorizado:
                    raise PermissionDenied(
                        'La sustancia {} sobrepasa el cupo autorizado, verifique'.format(
                            i.stock.sustancia.nombre)
                    )
                stock = i.stock
                stock.cantidad = stock.cantidad + i.cantidad
                stock.save()

                inv = Inventario()
                inv.compra_publica_detalle_id = i.id
                inv.cantidad_movimiento = i.cantidad
                inv.tipo_movimiento_id = tipo_movimiento.id
                inv.save()

    def revision_compra(self, observacion):
        with transaction.atomic():
            compras_publicas = self.object
            if compras_publicas.estado_compra.estado == 'almacenado':
                raise Exception(
                    "Compra ya almacenada en stock, no se puede actualizar"
                )
            compras_estado = EstadoTransaccion.objects.get(estado='revision')
            compras_publicas.estado_compra_id = compras_estado.id
            if observacion is None:
                observacion = ""
            compras_publicas.observacion = observacion
            compras_publicas.save()
