from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView

from app.settings import LOGIN_REDIRECT_URL
from core.base.mixins import ValidatePermissionRequiredMixin
from core.representantetecnico.models import Proveedor, ComprasPublicas


class EmpresaListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    permission_required = ('representantetecnico.view_proveedor',)
    model = Proveedor
    template_name = "empresa/list.html"

    def get(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.GET.get('action')
            if action is not None:
                if action == 'searchdata':
                    data = self.search_data()
                    return JsonResponse(data, safe=False)
        except Exception as e:
            messages.error(request, str(e))
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Empresas registradas"
        context['icontitle'] = "store-alt"
        context['create_url'] = reverse_lazy('rp:registroempresa')
        context['urls'] = [
            {"uridj": LOGIN_REDIRECT_URL, "uriname": "Home"},
            {"uridj": reverse_lazy('rp:empresas'), "uriname": "Empresas"}
        ]
        return context

    def search_data(self):
        data = []
        for i in Proveedor.objects.all():
            item = {'id': i.id, 'nombre': i.nombre, 'ruc': i.ruc, 'id_del': True}
            if ComprasPublicas.objects.filter(empresa_id=i.id).exists():
                item['id_del'] = False
            data.append(item)
        return data
