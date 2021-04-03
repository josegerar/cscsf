from django.forms import *

from core.login.models import User
from core.tecnicolaboratorio.models import Laboratorio


class LaboratorioForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.get('responsable').choices = User.get_choices_laboratory_worker

    class Meta:
        model = Laboratorio
        fields = '__all__'
        widgets = {
            'nombre': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el nombre del laboratorio',
                'autofocus': True,
                'autocomplete': 'off'
            }),
            'direccion': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese la dirección del laboratorio',
                'autocomplete': 'off'
            }),
            'responsable': Select(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%'
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
