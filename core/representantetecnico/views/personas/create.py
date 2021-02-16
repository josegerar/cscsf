from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView

from core.base.mixins import ValidatePermissionRequiredMixin
from core.representantetecnico.forms.formPersona import PersonaForm
from core.representantetecnico.models import Persona


class PersonaCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    permission_required = ('representantetecnico.add_persona',)
    model = Persona
    form_class = PersonaForm
    template_name = 'personas/create.html'
    success_url = reverse_lazy('rp:personas')
    url_redirect = success_url

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usertitle'] = "Representante Técnico"
        context['title'] = "Registrar personas"
        context['icontitle'] = "plus"
        context['url_list'] = self.success_url
        context['action'] = 'add'
        context['urls'] = [
            {"uridj": reverse_lazy('dashboard'), "uriname": "Home"},
            {"uridj": self.success_url, "uriname": "Personas"},
            {"uridj": reverse_lazy('rp:registropersonas'), "uriname": "Registro"}
        ]
        return context

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                data = form.save()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)
