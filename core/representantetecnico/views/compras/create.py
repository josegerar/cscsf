from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView

from core.base.mixins import ValidatePermissionRequiredMixin
from core.representantetecnico.forms.formCompra import ComprasForm
from core.representantetecnico.models import ComprasPublicas


class ComprasCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    permission_required = ('representantetecnico.add_compraspublicas',)#appname.action(add, change, delete view)_table
    model = ComprasPublicas
    form_class = ComprasForm
    template_name = 'compras/create.html'
    success_url = reverse_lazy('rp:compras')
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usertitle'] = "Representante Técnico"
        context['title'] = "Registrar compra"
        context['icontitle'] = "plus"
        context['url_create'] = reverse_lazy('rp:registrocompras')
        context['url_list'] = self.success_url
        context['action'] = 'add'
        context['urls'] = [
            {"uridj": reverse_lazy('dashboard'), "uriname": "Home"},
            {"uridj": self.success_url, "uriname": "Compras"},
            {"uridj": context['url_create'], "uriname": "Registro"}
        ]
        return context

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha realizado ninguna accion'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)