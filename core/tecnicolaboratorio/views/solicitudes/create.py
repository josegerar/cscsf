from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView

from app.settings import LOGIN_REDIRECT_URL
from core.base.mixins import ValidatePermissionRequiredMixin
from core.representantetecnico.models import Solicitud
from core.tecnicolaboratorio.forms.formSolicitud import SolicitudForm


class SolicitudCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    permission_required = ('representantetecnico.add_solicitud',)
    model = Solicitud
    form_class = SolicitudForm
    template_name = "solicitudtl/create.html"
    success_url = reverse_lazy("tl:solicitudes")
    url_redirect = success_url

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usertitle'] = "Representante Técnico"
        context['title'] = "Registro solicitudes de entrega sustancias"
        context['icontitle'] = "plus"
        context['url_list'] = self.success_url
        context['action'] = 'add'
        context['urls'] = [
            {"uridj": LOGIN_REDIRECT_URL, "uriname": "Home"},
            {"uridj": self.success_url, "uriname": "Solicitudes"},
            {"uridj": reverse_lazy('tl:registrosolicitud'), "uriname": "Registro"}
        ]
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
