from datetime import datetime

from django.forms import *
from django.utils import timezone

from core.representantetecnico.models import ComprasPublicas


class ComprasForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = ' form-control'
            if form.widget_type == 'select':
                form.field.widget.attrs['class'] = form.field.widget.attrs.get('class', '') + ' select2'
            form.field.widget.attrs['autocomplete'] = 'off'

    class Meta:
        model = ComprasPublicas
        fields = '__all__'
        # exclude = ['id', 'fecha_registro']
        widgets = {
            'convocatoria': NumberInput(
                attrs={
                    'type': 'number',
                    'placeholder': 'Ingrese el numero de convocatoria'
                }
            ),
            'llegada_bodega': DateInput(
                format='%Y-%m-%d',
                attrs={
                    'type': 'date',
                    'value': timezone.now().strftime('%Y-%m-%d')
                }
            ),
            'hora_llegada_bodega': TimeInput(
                attrs={
                    'type': 'time'
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
