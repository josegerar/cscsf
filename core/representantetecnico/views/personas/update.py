import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from app.settings import LOGIN_REDIRECT_URL
from core.base.mixins import ValidatePermissionRequiredMixin
from core.login.models import User
from core.representantetecnico.forms.formPersona import PersonaForm
from core.representantetecnico.models import Persona


class PersonasUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    permission_required = ('login.change_persona',)
    model = Persona
    form_class = PersonaForm
    template_name = 'personas/create.html'
    success_url = reverse_lazy('rp:personas')
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Actualizar personas"
        context['icontitle'] = "edit"
        context['url_list'] = self.success_url
        context['action'] = 'edit'
        context['urls'] = [
            {"uridj": LOGIN_REDIRECT_URL, "uriname": "Home"},
        ]
        if self.request.user.is_representative:
            context['title'] = "Personas"
            context['urls'].append({"uridj": reverse_lazy('rp:personas'), "uriname": "Personas"})
            context['urls'].append({"uridj": reverse_lazy('rp:registropersonas'), "uriname": "Registro"})
        elif self.request.user.is_laboratory_worker:
            context['title'] = "Investigadores / Docentes"
            context['urls'].append({"uridj": reverse_lazy('rp:personas'), "uriname": "Investigadores"})
            context['urls'].append({"uridj": reverse_lazy('rp:registropersonas'), "uriname": "Edicción"})
        return context

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST.get('action')
            if action == 'edit':
                form = self.get_form()
                if form.is_valid():
                    persona = form.instance
                    users_new = json.loads(request.POST['usuarios'])
                    if persona is not None and users_new is not None:
                        with transaction.atomic():
                            for user in persona.user_set.all():
                                for user_n in users_new:
                                    if user.id == user_n['id']:
                                        if user.email != user_n['email']:
                                            user.email = user_n['email']
                else:
                    data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)
