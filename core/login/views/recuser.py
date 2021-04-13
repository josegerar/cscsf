from django.core import mail
from django.http import JsonResponse
from django.template.loader import get_template
from django.templatetags.static import static
from django.views.generic import TemplateView

from app.settings import EMAIL_HOST_USER
from core.login.models import User


class RecuperarUser(TemplateView):
    template_name = "recuperarusuario.html"

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST.get('action')
            if action is not None:
                if action == 'sendUser':
                    self.send_user(request)
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data["error"] = str(e)
        return JsonResponse(data, safe=False)

    def send_user(self, request):
        correo = request.POST.get('correo')
        if correo is not None:
            if User.objects.filter(email=correo).exists() is False:
                raise Exception(
                    "No existe el nombre de usuario registrado, "
                    "pongase en contacto con el administrador del sistema para corregir"
                )
            users = User.objects.filter(email=correo)
            for user in users:
                template_email = get_template("correo/sendUser.html")
                context_pass = {"name": user.get_user_info(),
                                "username": user.username,
                                "urllogin": request.build_absolute_uri("/"),
                                "logo": request.build_absolute_uri(
                                    static('img/uteq/logoUTEQoriginal1.png'))}
                content_pass = template_email.render(context_pass)
                email_send = mail.EmailMultiAlternatives(
                    "Envio de correo",
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
            raise Exception('Datos incorrectos')
