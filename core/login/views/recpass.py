import random
import string

from django.conf import settings
from django.contrib.auth import password_validation
from django.contrib.auth.views import LoginView
from django.core import mail
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import redirect
from django.template.loader import get_template
from django.templatetags.static import static
from django.views.generic import TemplateView

from app.settings import EMAIL_HOST_USER
from core.login.models import User


class recuperarpass(TemplateView):
    template_name = "recuperarpass.html"

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST.get('action')
            if action is not None:
                if action == 'actChangePass':
                    pass1 = request.POST.get('pass')
                    pass2 = request.POST.get('pass2')
                    code = request.POST.get('codeConfirm')
                    usuario = request.POST.get('usuario')
                    if pass1 is not None and pass2 is not None and code is not None:
                        if User.objects.filter(username=usuario).exists() is False:
                            raise Exception(
                                "No existe el nombre de usuario registrado, "
                                "pongase en contacto con el administrador del sistema para corregir"
                            )
                        user = User.objects.get(username=usuario)
                        if pass1 == pass2:
                            if code == user.codeconfirm:
                                with transaction.atomic():
                                    password_validation.validate_password(pass1, user)
                                    user.codeconfirm = None
                                    user.set_password(pass1)
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
                                    emailsend_rest = email_send.send()
                                    if emailsend_rest != 1:
                                        raise Exception(
                                            "ha ocurrido un error al enviar el correo, "
                                            "por favor vuelva a intentarlo"
                                        )
                            else:
                                data['error'] = 'código erroreo'
                        else:
                            data['error'] = 'Las contraseñas no coinciden'
                    else:
                        data['error'] = 'Datos incorrectos'
                elif action == 'sendCodeConfirm':
                    usuario = request.POST.get('usuario')
                    if User.objects.filter(username=usuario).exists() is False:
                        raise Exception(
                            "No existe el nombre de usuario registrado, "
                            "pongase en contacto con el administrador del sistema para corregir"
                        )
                    user = User.objects.get(username=usuario)
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
                        emailsend_rest = email_send.send()
                        if emailsend_rest != 1:
                            raise Exception(
                                "ha ocurrido un error al enviar el correo, "
                                "por favor vuelva a intentarlo"
                            )
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data["error"] = str(e)
        return JsonResponse(data, safe=False)
