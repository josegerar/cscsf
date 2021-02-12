from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView

from core.representantetecnico.forms.formSolicitud import SolicitudForm
from core.representantetecnico.models import Solicitud


class SustanciaCreateView(CreateView):
    model = Solicitud
    form_class = SolicitudForm
    template_name = "solicitudentregasustancias.html"
    success_url = reverse_lazy("rp:listadosolicitudes")

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['urls'] = [
            {"uridj": reverse_lazy('rp:index'), "uriname": "Home"},
            {"uridj": reverse_lazy('rp:listadosolicitudes'), "uriname": "Solicitudes"},
            {"uridj": reverse_lazy('rp:entregasustancias'), "uriname": "Registro"}
        ]
        context['usertitle'] = "Representante Técnico"
        context['title'] = "Registro entrega sustancias"
        return context

    def post(self, request, *args, **kwargs):
        data = None
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                data = form.save()
            else:
                data = {}
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)
