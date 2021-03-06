from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView

from app.settings import LOGIN_REDIRECT_URL
from core.base.mixins import ValidatePermissionRequiredMixin
from core.representantetecnico.models import ComprasPublicas, EstadoTransaccion, Proveedor


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
                    data = self.search_data(type, id_s, request.user)
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

    def search_data(self, type, id_s, user):
        data = []
        if type == 'est':
            if user.is_grocer:
                query = ComprasPublicas.objects.filter(estado_compra_id=id_s, bodega__responsable_id=user.id)
            else:
                query = ComprasPublicas.objects.filter(estado_compra_id=id_s)
        elif type == 'conv':
            if user.is_grocer:
                query = ComprasPublicas.objects.filter(convocatoria=id_s, bodega__responsable_id=user.id)
            else:
                query = ComprasPublicas.objects.filter(convocatoria=id_s)
        elif type == 'emp':
            if user.is_grocer:
                query = ComprasPublicas.objects.filter(empresa_id=id_s, bodega__responsable_id=user.id)
            else:
                query = ComprasPublicas.objects.filter(empresa_id=id_s)
        else:
            if user.is_grocer:
                query = ComprasPublicas.objects.filter(bodega__responsable_id=user.id)
            else:
                query = ComprasPublicas.objects.all()
        for i in query:
            item = {'id': i.id, 'llegada_bodega': i.llegada_bodega,
                    'hora_llegada_bodega': i.hora_llegada_bodega,
                    'convocatoria': i.convocatoria, 'estado': i.estado_compra.estado,
                    'empresa': i.empresa.nombre}
            data.append(item)
        return data
