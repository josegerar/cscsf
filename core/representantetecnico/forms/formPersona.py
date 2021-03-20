from django.forms import *

from core.representantetecnico.models import Persona


class PersonaForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Persona
        fields = '__all__'
        exclude = ['tipo_persona']
        widgets = {
            'nombre': TextInput(
                attrs={
                    'placeholder': 'Ingrese los nombres',
                    'type': 'text',
                    'class': 'form-control',
                    'autocomplete': 'off'
                }
            ),
            'apellido': TextInput(
                attrs={
                    'placeholder': 'Ingrese los apellidos',
                    'type': 'text',
                    'class': 'form-control',
                    'autocomplete': 'off'
                }
            ),
            'cedula': NumberInput(
                attrs={
                    'placeholder': 'Ingrese el numero de cedula',
                    'type': 'text',
                    'minlength': 10,
                    'onkeypress': 'return event.charCode >= 48 && event.charCode <= 57',
                    'class': 'form-control',
                    'autocomplete': 'off'
                }
            )
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
