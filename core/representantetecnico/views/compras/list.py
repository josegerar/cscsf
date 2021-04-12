from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView

from app.settings import LOGIN_REDIRECT_URL
from core.base.mixins import ValidatePermissionRequiredMixin
from core.representantetecnico.models import ComprasPublicas, ComprasPublicasDetalle, EstadoTransaccion, \
    Proveedor


class ComprasListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    permission_required = ('representantetecnico.view_compraspublicas',)
    model = ComprasPublicas
    template_name = "compras/list.html"

    def get(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.GET.get('action')
            if action is not None:
                if action == 'searchdata':
                    id_s = request.GET.get('id')
                    type = request.GET.get('type')
                    data = []
                    if type == 'est':
                        if request.user.is_grocer:
                            query = ComprasPublicas.objects.filter(estado_compra_id=id_s,
                                                                   bodega__responsable_id=request.user.id)
                        else:
                            query = ComprasPublicas.objects.filter(estado_compra_id=id_s)
                    elif type == 'conv':
                        if request.user.is_grocer:
                            query = ComprasPublicas.objects.filter(convocatoria=id_s,
                                                                   bodega__responsable_id=request.user.id)
                        else:
                            query = ComprasPublicas.objects.filter(convocatoria=id_s)
                    elif type == 'emp':
                        if request.user.is_grocer:
                            query = ComprasPublicas.objects.filter(empresa_id=id_s,
                                                                   bodega__responsable_id=request.user.id)
                        else:
                            query = ComprasPublicas.objects.filter(empresa_id=id_s)
                    else:
                        if request.user.is_grocer:
                            query = ComprasPublicas.objects.filter(bodega__responsable_id=request.user.id)
                        else:
                            query = ComprasPublicas.objects.all()
                    for i in query:
                        item = {'id': i.id, 'llegada_bodega': i.llegada_bodega,
                                'hora_llegada_bodega': i.hora_llegada_bodega,
                                'convocatoria': i.convocatoria, 'estado': i.estado_compra.estado,
                                'empresa': i.empresa.nombre}
                        data.append(item)
                    return JsonResponse(data, safe=False)
                elif action == 'searchdetail':
                    data = []
                    id_comp = request.GET.get('id_comp')
                    detalle_compras = ComprasPublicasDetalle.objects.filter(compra_id=id_comp)
                    for dci in detalle_compras:
                        item = {'id': dci.id, 'cantidad': float(dci.cantidad),
                                'bodega_selected': {'id': dci.stock.bodega.id, 'text': dci.stock.bodega.nombre},
                                'stock': {'id': dci.stock.id,
                                          'cupo_autorizado': float(dci.stock.sustancia.cupo_autorizado),
                                          'value': dci.stock.sustancia.nombre,
                                          'unidad_medida': dci.stock.sustancia.unidad_medida.nombre,
                                          'cantidad_bodega': float(dci.stock.cantidad),
                                          'cupo_consumido': dci.stock.sustancia.get_cupo_consumido(
                                              timezone.now().year)}}
                        data.append(item)
                    return JsonResponse(data, safe=False)
        except Exception as e:
            data['error'] = str(e)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Compras registradas"
        context['icontitle'] = "store-alt"
        context['estados'] = EstadoTransaccion.objects.all()
        context['convocatorias'] = ComprasPublicas.objects.order_by('convocatoria').distinct('convocatoria').values(
            "convocatoria")
        context['empresas'] = Proveedor.objects.all()
        context['create_url'] = reverse_lazy('rp:registrocompras')
        context['urls'] = [
            {"uridj": LOGIN_REDIRECT_URL, "uriname": "Home"},
            {"uridj": reverse_lazy('rp:compras'), "uriname": "Compras"}
        ]
        return context
