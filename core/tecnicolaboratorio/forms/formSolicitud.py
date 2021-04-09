from django.forms import *

from core.login.models import Persona
from core.representantetecnico.models import Solicitud
from core.tecnicolaboratorio.models import Laboratorio


class SolicitudForm(ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)
        self.fields.get('laboratorio').choices = Laboratorio.get_choices_laboratory_user(self.request.user.id)
        self.fields.get('responsable_actividad').choices = Persona.get_choices_responsable_practica

    class Meta:
        model = Solicitud
        fields = '__all__'
        exclude = ['estado_solicitud', 'fecha_autorizacion', 'solicitante', 'observacion']
        widgets = {
            'laboratorio': Select(attrs={
                'class': 'form-control',
                'style': 'width: 100%'
            }),
            'bodega': Select(attrs={
                'class': 'form-control',
                'style': 'width: 100%'
            }),
            'tipo_actividad': Select(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%'
            }),
            'nombre_actividad': TextInput(
                attrs={
                    'placeholder': 'Ingrese el nombre del proyecto',
                    'type': 'text',
                    'class': 'form-control',
                    'autocomplete': 'off'
                }
            ),
            'responsable_actividad': Select(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%'
            }),
            'codigo_solicitud': TextInput(
                attrs={
                    'placeholder': 'Ingrese el codigo de la solicitud',
                    'type': 'text',
                    'class': 'form-control',
                    'autocomplete': 'off'
                }
            ),
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data
