from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView

from cssf.forms.rp.formEmpresa import EmpresaForm
from cssf.models import Proveedor

class EmpresaCreateView(CreateView):
    model = Proveedor
    form_class = EmpresaForm
    template_name = 'rp/empresa/create.html'
    success_url = reverse_lazy('rp:empresas')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usertitle'] = "Representante Técnico"
        context['title'] = "Registrar empresa"
        context['icontitle'] = "plus"
        context['urls'] = [
            {"uridj": reverse_lazy('rp:index'), "uriname": "Home"},
            {"uridj": reverse_lazy('rp:empresas'), "uriname": "Empresas"},
            {"uridj": reverse_lazy('rp:registroempresa'), "uriname": "Registro"}
        ]
        context['url_create'] = reverse_lazy('rp:registroempresa')
        context['url_list'] = reverse_lazy('rp:empresas')
        context['action'] = 'add'
        return context

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                data = form.save()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)