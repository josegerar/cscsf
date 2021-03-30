import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import mail
from django.db import transaction
from django.http import JsonResponse
from django.templatetags.static import static
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.template.loader import get_template

from app.settings import LOGIN_REDIRECT_URL, EMAIL_HOST_USER
from core.base.mixins import ValidatePermissionRequiredMixin
from core.login.models import Persona, User
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
        context['usertitle'] = "Representante Técnico"
        context['title'] = "Registrar investigador/docente"
        context['icontitle'] = "plus"
        context['url_list'] = self.success_url
        context['action'] = 'add'
        context['urls'] = [
            {"uridj": LOGIN_REDIRECT_URL, "uriname": "Home"},
            {"uridj": self.success_url, "uriname": "Personas"},
            {"uridj": reverse_lazy('rp:registropersonas'), "uriname": "Registro"}
        ]
        return context

    def post(self, request, *args, **kwargs):
        data = {}
        connection = None
        try:
            action = request.POST.get('action')
            if action is not None:
                if action == 'add':
                    form = self.get_form()
                    if form.is_valid():
                        persona = form.instance
                        if persona is not None:
                            with transaction.atomic():
                                usuarios = json.loads(request.POST['usuarios'])
                                is_valid_new_users = Persona.validate_new_users(users=usuarios)
                                if is_valid_new_users is False:
                                    raise Exception(
                                        'Ocurrio un error al crear un usuario, '
                                        'por favor verifique la información a registrar del usuario'
                                    )
                                template_email = get_template("correo/correo.html")
                                mails_sending = []
                                connection = mail.get_connection()
                                connection.open()
                                persona.save()
                                for user_item in usuarios:
                                    username = persona.get_username(key="")
                                    rol_selected = user_item["rol_selected"]
                                    estado_selected = user_item["estado_selected"]
                                    if username is None:
                                        raise Exception(
                                            'Ocurrio un error al crear un usuario, '
                                            'por favor verifique la información a registrar'
                                        )
                                    email_verified = User.validate_domain_email(user_item["email"])
                                    if email_verified is None:
                                        raise Exception(
                                            'Ocurrio un error al crear un usuario, '
                                            'correo electronico {} no valido'.format(user_item["email"])
                                        )
                                    email_person = User.verify_email_person(email_verified, persona.id)
                                    if email_person is False:
                                        raise Exception(
                                            'Ocurrio un error al crear un usuario, '
                                            'correo electronico {} ya utilizado por otro usuario'.format(
                                                user_item["email"])
                                        )
                                    new_user = User.objects.create_user(username=username, email=email_verified,
                                                                        password=persona.cedula)
                                    new_user.persona_id = persona.id
                                    if estado_selected["value"] == "habilitado":
                                        new_user.is_active = True
                                    else:
                                        new_user.is_active = False

                                    if rol_selected["value"] == "representante":
                                        new_user.is_representative = True
                                    elif rol_selected["value"] == "laboratorista":
                                        new_user.is_laboratory_worker = True
                                    elif rol_selected["value"] == "bodeguero":
                                        new_user.is_grocer = True

                                    context_email = {"name": "{} {}".format(persona.nombre, persona.apellido),
                                                     "username": new_user.username,
                                                     "email": new_user.email,
                                                     "urllogin": request.build_absolute_uri("/"),
                                                     "logo": request.build_absolute_uri(
                                                         static('img/uteq/logoUTEQoriginal1.png'))}
                                    content_email = template_email.render(context_email)
                                    email_send = mail.EmailMultiAlternatives(
                                        "Nuevo usuario",
                                        "Unidad de control de sustancias catalogadas, sujetas a fizcalización",
                                        EMAIL_HOST_USER,
                                        [email_verified]
                                    )
                                    email_send.attach_alternative(content_email, "text/html")
                                    mails_sending.append(email_send)
                                    new_user.save()
                                res_messages_email = connection.send_messages(mails_sending)
                                if res_messages_email != 1:
                                    raise Exception(
                                        'Ocurrio un error al intentar verificar un correo electronico, '
                                        'correo electronico {} no valido'.format(user_item["email"])
                                    )
                        else:
                            data['error'] = 'Ha ocurrido un error'
                    else:
                        data['error'] = form.errors
                else:
                    data['error'] = 'Ha ocurrido un error'
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        if connection is not None:
            connection.close()
        return JsonResponse(data)
