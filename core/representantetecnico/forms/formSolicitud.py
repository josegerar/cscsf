from django.forms import *

from core.login.models import User
from core.representantetecnico.models import Solicitud


class SolicitudForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.get('solicitante').choices = User.get_choices_user
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            if form.widget_type == 'select':
                form.field.widget.attrs['class'] = form.field.widget.attrs.get('class', '') + ' select2'
            form.field.widget.attrs['autocomplete'] = 'off'

    class Meta:
        model = Solicitud
        fields = '__all__'
        widgets = {
            'nombre_proyecto': TextInput(
                attrs={
                    'placeholder': 'Ingrese el nombre del proyecto',
                    'type': 'text'
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
