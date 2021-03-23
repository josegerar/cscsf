from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from app.settings import LOGIN_REDIRECT_URL
from core.base.mixins import ValidatePermissionRequiredMixin
from core.representantetecnico.forms.formSolicitud import SolicitudForm
from core.representantetecnico.models import Solicitud


class SolicitudUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    permission_required = ('representantetecnico.change_solicitud',)
    model = Solicitud
    form_class = SolicitudForm
    template_name = 'laboratorio/create.html'
    success_url = reverse_lazy('rp:solicitudes')
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object is not None:
            if self.object.estado_compra is not None:
                if self.object.estado_compra.estado == 'aprobado' or self.object.estado_compra.estado == 'entregado':
                    messages.error(request, 'solicitud de entrega de sustancia ya aprobado o entregado')
                    messages.error(request, 'No es posible su eliminación')
                    messages.error(request, 'Pongase en contacto con el administrador del sistema')
                    return HttpResponseRedirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usertitle'] = "Representante Técnico"
        context['title'] = "Actualizar solicitud"
        context['icontitle'] = "edit"
        context['url_list'] = self.success_url
        context['action'] = 'edit'
        context['urls'] = [
            {"uridj": LOGIN_REDIRECT_URL, "uriname": "Home"},
            {"uridj": self.success_url, "uriname": "Solicitudes"},
            {"uridj": reverse_lazy('rp:actualizacionsolicitud'), "uriname": "Edicción"}
        ]
        return context

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()
                data = form.save()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)
