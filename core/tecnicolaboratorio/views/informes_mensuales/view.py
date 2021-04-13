from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from core.base.mixins import ValidatePermissionRequiredMixin
from core.representantetecnico.models import InformesMensuales, EstadoTransaccion, TipoMovimientoInventario, Inventario


class InformeMensualView(LoginRequiredMixin, ValidatePermissionRequiredMixin, TemplateView):
    permission_required = ('representantetecnico.view_informesmensuales',)
    template_name = 'informesmensuales/view.html'
    url_redirect = reverse_lazy('tl:informesmensuales')

    def dispatch(self, request, *args, **kwargs):
        try:
            self.object = InformesMensuales.objects.get(pk=kwargs['pk'])
            return super().dispatch(request, *args, **kwargs)
        except Exception as e:
            messages.error(request, str(e))
        return HttpResponseRedirect(self.url_redirect)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url_list'] = self.url_redirect
        context['icontitle'] = 'eye'
        context['title'] = '{} {}'.format("Informe mensual", self.object.id)
        return context

    def get(self, request, *args, **kwargs):
        try:
            action = request.GET.get('action')
            if action is not None:
                if action == 'informe_detail':
                    data = self.get_informe_detail()
                    return JsonResponse(data, safe=False)
        except Exception as e:
            messages.error(request, str(e))
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST.get('action')
            if action is not None:
                if action == 'archivar_informe':
                    if request.user.is_laboratory_worker:
                        self.archivar_informe()
                    else:
                        data['error'] = 'No tiene permisos'
                else:
                    data['error'] = 'Ha ocurrido un error3'
            else:
                data['error'] = 'Ha ocurrido un error4'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_informe_detail(self):
        data = []
        for i in self.object.informesmensualesdetalle_set.all():
            data.append({
                'id': i.id,
                'stock': {'id': i.stock.id, 'nombre': i.stock.sustancia.nombre,
                          'unidad_medida': i.stock.sustancia.unidad_medida.nombre,
                          'cantidad_lab': i.stock.cantidad},
                'cantidad': i.cantidad
            })
        return data

    def archivar_informe(self):
        if self.object.estado_informe.estado == 'archivado':
            raise Exception("No se puede realizar acciones sobre este registro")
        with transaction.atomic():
            estado_transaccion = EstadoTransaccion.objects.get(estado="archivado")
            tipo_movimiento_del = TipoMovimientoInventario.objects.get(nombre='delete')
            informe = self.object
            informe.estado_informe_id = estado_transaccion.id
            informe.save()
            for det in informe.informesmensualesdetalle_set.all():
                cantidad_desglose = det.desgloseinfomemensualdetalle_set.all().aggregate(
                    cantidad_sum=Coalesce(Sum("cantidad"), 0))
                if cantidad_desglose["cantidad_sum"] != det.cantidad:
                    raise Exception("La cantidad desglosada total del consumo no coincide con "
                                    "la cantidad descrita en el detalle del informe para la "
                                    "sustancia {}".format(det.stock.sustancia.nombre))
                stock = det.stock
                stock.cantidad = stock.cantidad - det.cantidad
                stock.save()

                inv = Inventario()
                inv.informe_mensual_detalle_id = det.id
                inv.cantidad_movimiento = det.cantidad
                inv.tipo_movimiento_id = tipo_movimiento_del.id
                inv.save()
