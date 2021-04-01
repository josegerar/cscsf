from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models import Sum
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView

from app.settings import LOGIN_REDIRECT_URL
from core.base.mixins import ValidatePermissionRequiredMixin
from core.bodega.models import Inventario, TipoMovimientoInventario
from core.representantetecnico.models import InformesMensuales, InformesMensualesDetalle, Mes


class InformesMensualesListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    permission_required = ('representantetecnico.view_informesmensuales',)
    model = InformesMensuales
    template_name = "informesmensuales/list.html"

    def get(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.GET.get('action')
            if action is not None:
                if action == 'searchdata':
                    data = []
                    for i in InformesMensuales.objects.all():
                        item = {
                            'id': i.id,
                            'laboratorio': i.laboratorio.nombre,
                            'mes': i.mes.nombre,
                            'year': i.date_creation.year,
                            'is_editable': i.is_editable
                        }
                        data.append(item)
                    return JsonResponse(data, safe=False)
                elif action == 'informe_detail':
                    data = []
                    informe_id = request.GET.get('informe_id')
                    for i in InformesMensualesDetalle.objects.filter(informe_id=informe_id):
                        data.append({
                            'id': i.id,
                            'sustancia': {'id': i.stock.sustancia.id, 'nombre': i.stock.sustancia.nombre},
                            'unidad_medida': i.stock.sustancia.unidad_medida.nombre,
                            'cantidad_consumida': i.cantidad,
                            'cantidad_lab': i.stock.cantidad
                        })
                    return JsonResponse(data, safe=False)
                elif action == 'search_months_dsp':
                    data = []
                    year = request.GET.get('year')
                    for y in Mes.objects.all().exclude(informesmensuales__year=year):
                        data.append({'id': y.id, 'text': y.nombre})
                    return JsonResponse(data, safe=False)
        except Exception as e:
            data['error'] = str(e)
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST.get('action')
            if action is not None:
                if action == 'archivar_informe':
                    with transaction.atomic():
                        informe_id = request.POST.get('informe_id')
                        informe = InformesMensuales.objects.get(id=informe_id)
                        tipo_movimiento_del = TipoMovimientoInventario.objects.get(nombre='deletelab')
                        if informe is None and tipo_movimiento_del is not None:
                            raise Exception("Error al ejecutar la operación, recargue la pagina y vuelva a intentarlo")
                        for det in informe.informesmensualesdetalle_set.all():
                            cantidad_desglose = det.desgloseinfomemensualdetalle_set.all().aggregate(Sum("cantidad"))
                            if cantidad_desglose["cantidad__sum"] != det.cantidad:
                                raise Exception("La cantidad desglosada total del consumo no coincide con"
                                                "la cantidad descrita en el detalle del informe para la"
                                                "sustancia {}".format(det.stock.sustancia.nombre))
                            stock = det.stock
                            stock.cantidad = stock.cantidad - det.cantidad
                            stock.save()

                            inv = Inventario()
                            inv.stock_id = stock.id
                            inv.cantidad_movimiento = det.cantidad
                            inv.tipo_movimiento_id = tipo_movimiento_del.id
                            inv.save()

                        informe.is_editable = False
                        informe.save()
                else:
                    data['error'] = 'Ha ocurrido un error3'
            else:
                data['error'] = 'Ha ocurrido un error4'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Informes mensuales registrados"
        context['icontitle'] = "store-alt"
        context['create_url'] = reverse_lazy('tl:registroinformesmensuales')
        context['urls'] = [
            {"uridj": LOGIN_REDIRECT_URL, "uriname": "Home"},
            {"uridj": reverse_lazy('tl:informesmensuales'), "uriname": "Informes mesuales"}
        ]
        return context
