import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from app.settings import LOGIN_REDIRECT_URL
from core.base.mixins import ValidatePermissionRequiredMixin
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
        context['icontitle'] = "edit"
        context['url_list'] = self.success_url
        context['action'] = 'edit'
        context['urls'] = [
            {"uridj": LOGIN_REDIRECT_URL, "uriname": "Home"},
        ]
        if self.request.user.is_representative:
            context['title'] = "Personas"
            context['urls'].append({"uridj": reverse_lazy('rp:personas'), "uriname": "Personas"})
        elif self.request.user.is_laboratory_worker:
            context['title'] = "Actualizar Investigadores / Docentes"
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
                    self.actualiar_personas(persona, request)
                else:
                    data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def actualiar_personas(self, persona, request):
        with transaction.atomic():
            users_new = json.loads(request.POST['usuarios'])
            for user in persona.user_set.all():
                for user_n in users_new:
                    estado_selected = user_n["estado_selected"]
                    rol_selected = user_n["rol_selected"]
                    if user.id == user_n['id']:
                        if self.verify_rol_changed(rol_selected, request.user):
                            raise Exception("No puede cambiarse el rol a un usuario ya creado, "
                                            "verificar información")
                        if estado_selected["value"] == "habilitado":
                            user.is_active = True
                        else:
                            user.is_active = False
                        if user.email != user_n['email']:
                            user.email = user_n['email']
                            res_messages_email = user.send_email_user(request)
                            if res_messages_email != 1:
                                raise Exception(
                                    'Ocurrio un error al intentar verificar un correo electronico, '
                                    'correo electronico {} no valido'.format(user["email"])
                                )
                        user.save()
                        break
            for user_n in users_new:
                if user_n['id'] == -1:
                    rol_selected = user_n["rol_selected"]
                    estado_selected = user_n["estado_selected"]
                    persona.create_custom_user(request, rol_selected, estado_selected,
                                               user_n["email"])

    def verify_rol_changed(self, rol_selected, user):
        if rol_selected["value"] == "representante":
            if user.is_representative:
                return False
        elif rol_selected["value"] == "laboratorista":
            if user.is_laboratory_worker:
                return False
        elif rol_selected["value"] == "bodeguero":
            if user.is_grocer:
                return False
        return False
