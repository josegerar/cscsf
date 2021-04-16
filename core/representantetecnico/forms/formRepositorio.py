from django.forms import ModelForm

from core.representantetecnico.models import Repositorio


class RepositorioForm(ModelForm):
    class Meta:
        model = Repositorio
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
