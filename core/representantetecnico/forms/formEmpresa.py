from django.forms import *

from core.representantetecnico.models import Proveedor


class EmpresaForm(ModelForm):

    class Meta:
        model = Proveedor
        fields = '__all__'
        widgets = {
            'nombre': TextInput(attrs={
                'type': 'text',
                'class': 'form-control',
                'autocomplete': 'off',
                'placeholder': 'Ingrese el nombre de la empresa'
            }),
            'ruc': NumberInput(attrs={
                'placeholder': 'Ingrese el RUC de la empresa',
                'type': 'text',
                'minlength': 13,
                'class': 'form-control',
                'autocomplete': 'off',
                'onkeypress': 'return event.charCode >= 48 && event.charCode <= 57'
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
