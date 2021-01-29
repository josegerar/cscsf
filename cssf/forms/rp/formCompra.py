from django.forms import *

from cssf.models import ComprasPublicas

class ComprasForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'


    class Meta:
        model = ComprasPublicas
        fields = '__all__'
        #exclude = ['id', 'fecha_registro']
        widgets = {
            'convocatoria': NumberInput(
                attrs={
                    'type': 'number',
                    'placeholder': 'Ingrese el numero de convocatoria'
                }
            ),
            'llegada_bodega': DateInput(
                attrs={
                    'type': 'date'
                }
            ),
            'hora_llegada_bodega': TimeInput(
                attrs={
                    'type': 'time'
                }
            )
        }