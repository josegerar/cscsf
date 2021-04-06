from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import DeleteView

from app.settings import LOGIN_REDIRECT_URL
from core.base.mixins import ValidatePermissionRequiredMixin
from core.login.models import User
from core.representantetecnico.models import Persona, Solicitud


class PersonasDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    permission_required = ('login.delete_persona',)
    model = Persona
    template_name = 'delete.html'
    success_url = reverse_lazy('rp:personas')
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object:
            if User.objects.filter(persona_id=self.object.id).exists() or Solicitud.objects.filter(
                    responsable_actividad_id=self.object.id).exists():
                messages.error(request, 'No es posible eliminar este registro')
                messages.error(request, 'Pongase en contacto con el administrador del sistema')
                return HttpResponseRedirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            if User.objects.filter(persona_id=self.object.id).exists():
                raise Exception(
                    'No es posible eliminar este registro'
                    'Pongase en contacto con el administrador del sistema'
                )
            self.object.delete()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Eliminar personas"
        context['icontitle'] = "trash-alt"
        context['url_list'] = self.success_url
        context['urls'] = [
            {"uridj": LOGIN_REDIRECT_URL, "uriname": "Home"},
            {"uridj": self.success_url, "uriname": "Personas"},
            {"uridj": reverse_lazy('rp:registropersonas'), "uriname": "Eliminar"}
        ]
        return context
