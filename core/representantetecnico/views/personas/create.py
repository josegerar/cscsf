import json

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView

from app.settings import LOGIN_REDIRECT_URL
from core.base.mixins import ValidatePermissionRequiredMixin
from core.login.models import Persona
from core.representantetecnico.forms.formPersona import PersonaForm


class PersonaCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    permission_required = ('login.add_persona',)
    model = Persona
    form_class = PersonaForm
    template_name = 'personas/create.html'
    success_url = reverse_lazy('rp:personas')
    url_redirect = success_url

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['icontitle'] = "plus"
        context['url_list'] = self.success_url
        context['action'] = 'add'
        context['urls'] = [
            {"uridj": LOGIN_REDIRECT_URL, "uriname": "Home"},
        ]
        if self.request.user.is_representative:
            context['title'] = "Registrar Personas"
            context['urls'].append({"uridj": reverse_lazy('rp:personas'), "uriname": "Personas"})
        elif self.request.user.is_laboratory_worker:
            context['title'] = "Registrar Investigadores / Docentes"
            context['urls'].append({"uridj": reverse_lazy('rp:personas'), "uriname": "Investigadores"})
        context['urls'].append({"uridj": reverse_lazy('rp:registropersonas'), "uriname": "Registro"})
        return context

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST.get('action')
            if action is not None:
                if action == 'add':
                    form = self.get_form()
                    if form.is_valid():
                        persona = form.instance
                        self.create_persona(persona, request)
                    else:
                        data['error'] = form.errors
                else:
                    data['error'] = 'Ha ocurrido un error'
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            messages.error(request, str(e))
        return JsonResponse(data)

    def create_persona(self, persona, request):
        with transaction.atomic():
            persona.save()
            if request.user.is_representative:
                self.create_users_persona(persona, request)

    def create_users_persona(self, persona, request):
        usuarios = json.loads(request.POST.get('usuarios'))
        is_valid_new_users = Persona.validate_new_users(users=usuarios)
        if is_valid_new_users is False:
            raise Exception(
                'Ocurrio un error al crear un usuario, '
                'por favor verifique la información a registrar del usuario'
            )
        for user_item in usuarios:
            rol_selected = user_item["rol_selected"]
            estado_selected = user_item["estado_selected"]
            persona.create_custom_user(request, rol_selected, estado_selected,
                                       user_item["email"])
