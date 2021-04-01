import random
import string

from django.contrib.auth import password_validation
from django.contrib.auth.hashers import check_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import mail
from django.db import transaction
from django.http import JsonResponse
from django.template.loader import get_template
from django.templatetags.static import static
from django.views.generic import TemplateView

from app.settings import EMAIL_HOST_USER
from core.base.mixins import IsUserUCSCSF
from core.representantetecnico.forms.formPersona import PersonaForm


class DashBoard(LoginRequiredMixin, IsUserUCSCSF, TemplateView):
    template_name = 'dashboard/dashboard.html'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST.get('action')
            if action is not None:
                if action == 'actChangePass':
                    pass_act = request.POST.get('passact')
                    pass1 = request.POST.get('pass')
                    pass2 = request.POST.get('pass2')
                    code = request.POST.get('codeConfirm')
                    if pass1 is not None and pass2 is not None and code is not None and pass_act is not None:
                        user = request.user
                        if check_password(pass_act, user.password):
                            if pass1 == pass2:
                                if code == user.codeconfirm:
                                    with transaction.atomic():
                                        password_validation.validate_password(pass1, user)
                                        user.codeconfirm = None
                                        user.set_password(pass1)
                                        user.is_pass_update = True
                                        user.save()
                                        template_email = get_template("correo/confirmcorrectpass.html")
                                        context_pass = {"name": user.username,
                                                        "urllogin": request.build_absolute_uri("/"),
                                                        "logo": request.build_absolute_uri(
                                                            static('img/uteq/logoUTEQoriginal1.png'))}
                                        content_pass = template_email.render(context_pass)
                                        email_send = mail.EmailMultiAlternatives(
                                            "Cambio de contraseña",
                                            "Unidad de control de sustancias catalogadas, sujetas a fizcalización",
                                            EMAIL_HOST_USER,
                                            [user.email]
                                        )
                                        email_send.attach_alternative(content_pass, "text/html")
                                        email_send.send()
                                else:
                                    data['error'] = 'código erroreo'
                            else:
                                data['error'] = 'Las contraseñas no coinciden'
                        else:
                            data['error'] = 'La contraseña actual escrita es incorrecta'
                    else:
                        data['error'] = 'Datos incorrectos'
                elif action == 'sendCodeConfirm':
                    user = request.user
                    codeconfirmacion = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(10))
                    with transaction.atomic():
                        user.codeconfirm = codeconfirmacion
                        user.save()
                        template_email = get_template("correo/changePass.html")
                        context_pass = {"name": user.username,
                                        "codeconfirm": codeconfirmacion,
                                        "logo": request.build_absolute_uri(
                                            static('img/uteq/logoUTEQoriginal1.png'))}
                        content_pass = template_email.render(context_pass)
                        email_send = mail.EmailMultiAlternatives(
                            "Codigo de confirmación",
                            "Unidad de control de sustancias catalogadas, sujetas a fizcalización",
                            EMAIL_HOST_USER,
                            [user.email]
                        )
                        email_send.attach_alternative(content_pass, "text/html")
                        email_send.send()
                elif action == 'update_info_user':
                    with transaction.atomic():
                        user = request.user
                        persona_form = PersonaForm(request.POST, request.FILES, instance=user.persona)
                        if persona_form is not None:
                            persona = persona_form.instance
                            persona.is_info_update = True
                            persona.save()
                            if user.persona is None:
                                user.persona_id = persona.id
                                user.save()
                        else:
                            raise Exception(
                                "Ha ocurrido un error al leer los datos, por favor vuelva a ejecutar la operación"
                            )
                else:
                    data['error'] = 'Datos incorrectos'
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data["error"] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Dashboard"
        return context
