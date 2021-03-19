from django.forms import *

from core.login.models import User
from core.representantetecnico.models import Solicitud


class SolicitudForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.get('solicitante').choices = User.get_choices_laboratory_worker

    class Meta:
        model = Solicitud
        fields = '__all__'
        widgets = {
            'solicitante': Select(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%',
                'autofocus': True
            }),
            'laboratorio': Select(attrs={
                'class': 'form-control select2',
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
                    'class': 'form-control'
                }
            ),
            'responsable_actividad': Select(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%'
            }),
            'documento_solicitud': FileInput(attrs={
                'class': 'form-control'
            })
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
