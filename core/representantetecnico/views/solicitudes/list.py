from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView

from core.representantetecnico.models import Solicitud


class SolicitudListView(ListView):
    model = Solicitud
    template_name = "listarsolicitudesentregasustancias.html"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['urls'] = [
            {"uridj": reverse_lazy('rp:index'), "uriname": "Home"},
            {"uridj": reverse_lazy('rp:listadosolicitudes'), "uriname": "Solicitudes"}
        ]
        context['usertitle'] = "Representante Técnico"
        context['title'] = "Solicitudes resgistradas"
        return context
