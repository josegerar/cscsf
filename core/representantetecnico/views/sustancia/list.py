from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView

from core.bodega.models import Sustancia


class SustanciaListView(ListView):
    model = Sustancia
    template_name = "listarstocksustancias.html"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['urls'] = [
            {"uridj": reverse_lazy('rp:index'), "uriname": "Home"},
            {"uridj": reverse_lazy('rp:inventario'), "uriname": "Inventario"}
        ]
        context['usertitle'] = "Representante Técnico"
        context['title'] = "Inventario"
        return context
