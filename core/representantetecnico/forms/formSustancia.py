from django.forms import *

from core.bodega.models import Sustancia


class SustanciaForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            if form.widget_type == 'select':
                form.field.widget.attrs['class'] = form.field.widget.attrs.get('class', '') + ' select2'
            form.field.widget.attrs['autocomplete'] = 'off'

    class Meta:
        model = Sustancia
        fields = '__all__'

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
