from django.forms import *

from core.representantetecnico.models import DesgloseInfomeMensualDetalle


class DesgloseSustanciaInformeMensualForm(ModelForm):
    class Meta:
        model = DesgloseInfomeMensualDetalle
        fields = '__all__'
        exclude = ['informe_mensual_detalle']
        widgets = {
            'solicitud': Select(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%'
            }),
            'cantidad': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Cantidad'
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
