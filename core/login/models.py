from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from django.forms import model_to_dict
from django.utils.translation import gettext_lazy as _
from django.templatetags.static import static
from django.core import mail
from django.template.loader import get_template

from app.settings import MEDIA_URL, STATIC_URL, EMAIL_HOST_USER
from core.base.models import BaseModel


class Persona(BaseModel):
    nombre = models.CharField(max_length=100, verbose_name="Nombres", default="")
    apellido = models.CharField(max_length=100, verbose_name="Apellidos")
    cedula = models.CharField(max_length=10, verbose_name="Cedula", unique=True)
    telefono = models.CharField(max_length=10, verbose_name="Telefono", null=True, blank=True)
    imagen = models.ImageField(upload_to="users/%Y/%m/%d", null=True, blank=True)
    is_active = models.BooleanField(default=True, editable=False)
    is_info_update = models.BooleanField(default=False, editable=False)

    def __str__(self):
        return "{} {} - {}".format(self.nombre, self.apellido, self.cedula)

    def get_username(self, key=""):
        parts = self.get_names_part()
        if parts is not None:
            username = parts[0][0:1]
            username += parts[2]
            username += parts[3][0:1]
            username += key
            username = str(username).lower()
            username_temp = username
            count = 0
            while self.username_exists(username):
                count += 1
                username = username_temp + str(count)
            return username
        return None

    def get_names_part(self):
        parts = ["", "", "", ""]
        nombre_array = self.nombre.strip().split(sep=" ")
        apellido_array = self.apellido.strip().split(sep=" ")
        if len(nombre_array) >= 1:
            parts[0] = nombre_array[0]
        if len(nombre_array) >= 2:
            parts[1] = nombre_array[1]
        if len(apellido_array) >= 1:
            parts[2] = apellido_array[0]
        if len(apellido_array) >= 2:
            parts[3] = apellido_array[1]
        return parts

    def create_custom_user(self, request, rol_selected, estado_selected, email):
        username = self.get_username(key="")
        if username is None:
            raise Exception(
                'Ocurrio un error al crear un usuario, '
                'por favor verifique la información a registrar'
            )
        email_verified = User.validate_domain_email(email)
        if email_verified is None:
            raise Exception(
                'Ocurrio un error al crear un usuario, '
                'correo electronico {} no valido. Debe ingresar '
                'un correo electronico institucional'.format(email)
            )
        email_person = User.verify_email_person(email_verified, self.id)
        if email_person is False:
            raise Exception(
                'Ocurrio un error al crear un usuario, este correo electronico '
                '{} ya utilizado por otro usuario del sistema'.format(
                    email)
            )
        new_user = User.objects.create_user(username=username, email=email_verified,
                                            password=self.cedula)
        new_user.persona_id = self.id
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
        res_messages_email = new_user.send_email_user(request)
        if res_messages_email != 1:
            raise Exception(
                'Ocurrio un error al intentar verificar un correo electronico, '
                'correo electronico {} no valido'.format(email)
            )
        new_user.save()

    def get_imagen(self):
        if self.imagen:
            return '{}{}'.format(MEDIA_URL, self.imagen)
        else:
            return '{}{}'.format(STATIC_URL, 'img/user.png')

    @staticmethod
    def username_exists(username):
        if User.objects.filter(username=username).exists():
            return True
        return False

    @staticmethod
    def validate_new_users(users):
        list_roles = ["representante", "laboratorista", "bodeguero"]
        list_roles_temp = []
        is_valid = True

        if len(users) > 3:
            return False

        for item in users:
            rol_selected = item["rol_selected"]
            if rol_selected['value'] in list_roles_temp:
                is_valid = False
                break
            if rol_selected['value'] in list_roles:
                list_roles_temp.append(rol_selected['value'])
            else:
                is_valid = False
                break
        return is_valid

    @staticmethod
    def get_choices_responsable_practica():
        choices = [('', '---------')]
        choices += [(p.id, p.__str__()) for p in Persona.objects.filter(user__persona_id=None)]
        return choices

    class Meta:
        verbose_name = "Persona"
        verbose_name_plural = "Personas"
        db_table = "persona"
        ordering = ["id"]


class User(AbstractUser, BaseModel):
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE, verbose_name="Persona", null=True)
    is_pass_update = models.BooleanField(default=False, editable=False)
    codeconfirm = models.CharField(max_length=200, null=True, blank=True)
    is_representative = models.BooleanField(
        _('Es representante técnico'),
        default=False,
        help_text=_('Indica si el usuario es Representante tecnico')
    )
    is_laboratory_worker = models.BooleanField(
        _('Es tecnico de laboratorio'),
        default=False,
        help_text=_('Indica si el usuario es Técnico de laboratorio')
    )
    is_grocer = models.BooleanField(
        _('Es bodegero'),
        default=False,
        help_text=_('Indica si el usuario es Bodeguero')
    )

    def __str__(self):
        return self.username

    @staticmethod
    def get_choices_user():
        choices = [('', '---------')]
        choices += [(o.id, o.get_user_info()) for o in User.objects.all()]
        return choices

    @staticmethod
    def get_choices_laboratory_worker():
        choices = [('', '---------')]
        choices += [(o.id, o.get_user_info()) for o in User.objects.filter(is_laboratory_worker=True)]
        return choices

    @staticmethod
    def get_choices_grocer():
        choices = [('', '---------')]
        choices += [(o.id, o.get_user_info()) for o in User.objects.filter(is_grocer=True)]
        return choices

    @staticmethod
    def verify_email_person(email, person_id):
        if User.objects.filter(email=email).exclude(persona_id=person_id).exists():
            return False
        return True

    @staticmethod
    def validate_domain_email(email):
        email = str(email).strip()
        if email.__contains__("@"):
            domain = email.split('@')[1]
            domain_list = ["uteq.edu.ec", ]
            if domain in domain_list:
                return email
        return None

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Call the "real" save() method.
        group = None
        if self.is_grocer is True:
            group = Group.objects.get(name__iexact='bodega')
        elif self.is_laboratory_worker is True:
            group = Group.objects.get(name__iexact='laboratorio')
        elif self.is_representative is True:
            group = Group.objects.get(name__iexact='representante')
        if group is not None:
            if self.groups.filter(name=group.name).exists() is False:
                self.groups.add(group)

    def send_email_user(self, request):
        if self.persona is not None:
            template_email = get_template("correo/correo.html")
            context_email = {"name": "{} {}".format(self.persona.nombre, self.persona.apellido),
                             "username": self.username,
                             "email": self.email,
                             "urllogin": request.build_absolute_uri("/"),
                             "logo": request.build_absolute_uri(
                                 static('img/uteq/logoUTEQoriginal1.png'))}
            content_email = template_email.render(context_email)
            email_send = mail.EmailMultiAlternatives(
                "Nuevo usuario",
                "Unidad de control de sustancias catalogadas, sujetas a fizcalización",
                EMAIL_HOST_USER,
                [self.email]
            )
            email_send.attach_alternative(content_email, "text/html")
            return email_send.send()
        return 0

    def get_user_info(self):
        if self.persona is not None:
            return self.persona.__str__()
        else:
            return self.username

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
        db_table = "auth_user"
        ordering = ["id"]
