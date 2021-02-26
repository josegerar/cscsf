from datetime import datetime

from django.forms import *
from django.utils import timezone

from core.representantetecnico.models import ComprasPublicas


class ComprasForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # for form in self.visible_fields():
        #     form.field.widget.attrs['class'] = ' form-control'
        #     if form.widget_type == 'select':
        #         form.field.widget.attrs['class'] = form.field.widget.attrs.get('class', '') + ' select2'
        #     form.field.widget.attrs['autocomplete'] = 'off'

    class Meta:
        model = ComprasPublicas
        fields = '__all__'
        # exclude = ['id', 'fecha_registro']
        widgets = {
            'empresa': Select(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%',
                'autofocus': True
            }),
            'llegada_bodega': DateInput(format='%Y-%m-%d', attrs={
                'class': 'form-control datetimepicker-input',
                'data-target': '#llegada_bodega',
                'data-toggle': 'datetimepicker',
                'autocomplete': 'off',
                'value': datetime.now().strftime('%Y-%m-%d')
            }),
            'hora_llegada_bodega': TimeInput(format='%H:%M:%S', attrs={
                'class': 'form-control datetimepicker-input',
                'data-target': '#hora_llegada_bodega',
                'data-toggle': 'datetimepicker',
                'autocomplete': 'off',
                'value': datetime.now().strftime("%H:%M:%S")
            }),
            'convocatoria': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el numero de convocatoria'
            }),
            'responsable_entrega': Select(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%'
            }),
            'pedido_compras_publicas': FileInput(attrs={
                'class': 'form-control',
            }),
            'guia_transporte': FileInput(attrs={
                'class': 'form-control',
            }),
            'factura': FileInput(attrs={
                'class': 'form-control',
            }),
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
