from django.forms import *

from cssf.models import ComprasPublicas

class ComprasForm(ModelForm):
    class Meta:
        model = ComprasPublicas
        fields = '__all__'
        #exclude = ['id', 'fecha_registro']
        widgets = {
            'convocatoria': NumberInput(
                attrs={
                    'class': 'form-control',
                    'type': 'number',
                    'placeholder': 'Ingrese el numero de convocatoria'
                }
            ),
            'llegada_bodega': DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date'
                }
            ),
            'hora_llegada_bodega': TimeInput(
                attrs={
                    'class': 'form-control',
                    'type': 'time'
                }
            ),
            'id_empresa': Select(
                attrs={
                    'class': 'form-control'
                }
            ),
            'id_responsable_entrega_compras': Select(
                attrs={
                    'class': 'form-control'
                }
            ),
            'id_transportista_compras': Select(
                attrs={
                    'class': 'form-control'
                }
            )
        }