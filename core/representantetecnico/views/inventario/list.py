from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView

from core.bodega.models import Inventario
from core.representantetecnico.mixins import IsTechnicalRepresentative


class InventarioListView(LoginRequiredMixin, IsTechnicalRepresentative, ListView):
    model = Inventario
    template_name = "listarmovimientosinventario.html"

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['urls'] = [
            {"uridj": reverse_lazy('rp:index'), "uriname": "Home"},
            {"uridj": reverse_lazy('rp:inventario'), "uriname": "Inventario"},
            {"uridj": reverse_lazy('rp:movimientoinventario'), "uriname": "Movimientos"}
        ]
        context['usertitle'] = "Representante Técnico"
        context['title'] = "Movimientos inventario"
        return context
