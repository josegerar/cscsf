from datetime import datetime

from django.forms import *

from core.representantetecnico.models import InformesMensuales
from core.tecnicolaboratorio.models import Laboratorio


class InformeMensualForm(ModelForm):
    year = CharField(widget=TextInput(attrs={
        'class': 'form-control',
        'value': ''
    }))

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)
        if self.instance is not None:
            self.fields.get('year').widget.attrs['value'] = self.instance.date_creation.year
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
            'mes': Select(attrs={
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
