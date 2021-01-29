from django.urls import reverse_lazy
from django.views.generic import CreateView

from cssf.forms.rp.formCompra import ComprasForm
from cssf.models import ComprasPublicas, Laboratorio


class ComprasCreateView(CreateView):
    model = ComprasPublicas
    form_class = ComprasForm
    template_name = 'rp/registrocompras.html'
    success_url = reverse_lazy('rp:compras')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usertitle'] = "Representante Técnico"
        context['title'] = "Registrar compra"
        context['icontitle'] = "plus"
        context['laboratorios'] = Laboratorio.objects.all()
        context['urls'] = [
            {
                "uridj": "rp:index",
                "uriname": "Home"
            },
            {
                "uridj": "rp:compras",
                "uriname": "Compras"
            },
            {
                "uridj": "rp:registrocompras",
                "uriname": "Registro"
            }
        ]
        return context