from datetime import datetime

from django.forms import *

from core.representantetecnico.models import InformesMensuales
from core.tecnicolaboratorio.models import Laboratorio


class InformeMensualForm(ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)
        self.fields.get('laboratorio').choices = Laboratorio.get_choices_laboratory_user(self.request.user.id)

    class Meta:
        model = InformesMensuales
        fields = '__all__'
        exclude = ['laboratorista']
        widgets = {
            'laboratorio': Select(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%'
            }),
            'fecha_inicio': DateInput(format='%Y-%m-%d', attrs={
                'class': 'form-control datetimepicker-input',
                'data-target': '#fecha_inicio',
                'data-toggle': 'datetimepicker',
                'autocomplete': 'off',
                'value': datetime.now().strftime('%Y-%m-%d')
            }),
            'fecha_fin': DateInput(format='%Y-%m-%d', attrs={
                'class': 'form-control datetimepicker-input',
                'data-target': '#fecha_fin',
                'data-toggle': 'datetimepicker',
                'autocomplete': 'off',
                'value': datetime.now().strftime('%Y-%m-%d')
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
