from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import DeleteView

from app.settings import LOGIN_REDIRECT_URL
from core.base.mixins import ValidatePermissionRequiredMixin
from core.representantetecnico.models import Solicitud


class SolicitudDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    permission_required = ('representantetecnico.delete_solicitud',)
    model = Solicitud
    template_name = 'delete.html'
    success_url = reverse_lazy('tl:solicitudes')
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object is not None:
            if self.object.estado_solicitud is not None:
                if self.object.estado_solicitud.estado in ['almacenado', 'entregado', 'aprobado', 'recibido']:
                    messages.error(request, 'solicitud de entrega de sustancia ya aprobado o entregado')
                    messages.error(request, 'No es posible su eliminación')
                    messages.error(request, 'Pongase en contacto con el administrador del sistema')
                    return HttpResponseRedirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usertitle'] = "Representante Técnico"
        context['title'] = "Eliminar solicitud"
        context['icontitle'] = "trash-alt"
        context['url_list'] = self.success_url
        context['urls'] = [
            {"uridj": LOGIN_REDIRECT_URL, "uriname": "Home"},
            {"uridj": self.success_url, "uriname": "Solicitudes"},
            {"uridj": reverse_lazy('tl:eliminarsolicitud'), "uriname": "Eliminar"}
        ]
        return context