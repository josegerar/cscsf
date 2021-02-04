from django.forms import *

from cssf.models import Persona


class PersonaForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'

    class Meta:
        model = Persona
        fields = '__all__'
        widgets = {
            'nombre': TextInput(
                attrs={
                    'placeholder': 'Ingrese los nombres',
                    'type': 'text'
                }
            ),
            'apellido': TextInput(
                attrs={
                    'placeholder': 'Ingrese los apellidos',
                    'type': 'text'
                }
            ),
            'cedula': NumberInput(
                attrs={
                    'placeholder': 'Ingrese el numero de cedula',
                    'type': 'number'
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