from django.forms import *

from core.bodega.models import Sustancia

from django.utils.translation import gettext_lazy as _


class SustanciaForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        cantidad_cleaned = float(cleaned_data.get("cantidad"))
        cupo_autorizado_cleaned = float(cleaned_data.get("cupo_autorizado"))

        if cantidad_cleaned is not None and cupo_autorizado_cleaned is not None:
            if cantidad_cleaned > cupo_autorizado_cleaned:
                raise ValidationError(
                    _('Valor invalido: %(value)s La cantidad debe ser menor o igual al cupo autorizado'),
                    params={'value': cantidad_cleaned},
                )

    class Meta:
        model = Sustancia
        fields = '__all__'
        widgets = {
            'nombre': TextInput(attrs={
                'class': 'form-control',
                'autocomplete': 'off',
                'autofocus': 'true'
            }),
            'unidad_medida': Select(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%'
            }),
            'descripcion': Textarea(attrs={
                'class': 'form-control',
                'rows': "5"
            }),
            'cantidad': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese la cantidad actual de sustancia'
            }),
            'cupo_autorizado': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Cupo autorizado de sustancia'
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
