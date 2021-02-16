from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import DeleteView

from core.base.mixins import ValidatePermissionRequiredMixin
from core.representantetecnico.models import ComprasPublicas, Proveedor


class EmpresaDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    permission_required = ('representantetecnico.delete_proveedor',)
    model = Proveedor
    template_name = 'empresa/delete.html'
    success_url = reverse_lazy('rp:empresas')
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usertitle'] = "Representante Técnico"
        context['title'] = "Eliminar empresa"
        context['icontitle'] = "trash-alt"
        context['url_list'] = self.success_url
        context['urls'] = [
            {"uridj": reverse_lazy('dashboard'), "uriname": "Home"},
            {"uridj": self.success_url, "uriname": "Empresas"},
            {"uridj": reverse_lazy('rp:registroempresa'), "uriname": "Registro"}
        ]
        return context
