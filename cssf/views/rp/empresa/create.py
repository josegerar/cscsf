from django.urls import reverse_lazy
from django.views.generic import CreateView

from cssf.forms.rp.formEmpresa import EmpresaForm
from cssf.models import Proveedor


class EmpresaCreateView(CreateView):
    model = Proveedor
    form_class = EmpresaForm
    template_name = 'rp/empresa/create.html'
    success_url = reverse_lazy('rp:registroempresa')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usertitle'] = "Representante Técnico"
        context['title'] = "Registrar empresa"
        context['icontitle'] = "plus"
        context['urls'] = [
            {
                "uridj": "rp:index",
                "uriname": "Home"
            },
            {
                "uridj": "rp:empresas",
                "uriname": "Empresas"
            },
            {
                "uridj": "rp:registroempresa",
                "uriname": "Registro"
            }
        ]
        return context