from django.forms import *

from core.representantetecnico.models import Proveedor


class EmpresaForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'

    class Meta:
        model = Proveedor
        fields = '__all__'
        widgets = {
            'nombre': TextInput(
                attrs={
                    'type': 'text',
                    'placeholder': 'Ingrese el nombre de la empresa'
                }
            ),
            'ruc': NumberInput(
                attrs={
                    'type': 'number',
                    'placeholder': 'Ingrese el RUC de la empresa',
                    'minlength': 13
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