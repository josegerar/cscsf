from django.forms import *

from core.login.models import User
from core.tecnicolaboratorio.models import Laboratorio


class LaboratorioForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.get('responsable').choices = User.get_choices_laboratory_worker
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            if form.widget_type == 'select':
                form.field.widget.attrs['class'] = form.field.widget.attrs.get('class', '') + ' select2'
            form.field.widget.attrs['autocomplete'] = 'off'

    class Meta:
        model = Laboratorio
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
