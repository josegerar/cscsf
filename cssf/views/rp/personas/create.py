from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView

from cssf.forms.rp.formPersona import PersonaForm
from cssf.models import Persona


class PersonaCreateView(CreateView):
    model = Persona
    form_class = PersonaForm
    template_name = 'rp/personas/create.html'
    success_url = reverse_lazy('rp:personas')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usertitle'] = "Representante Técnico"
        context['title'] = "Registrar personas externas"
        context['icontitle'] = "plus"
        context['urls'] = [
            {"uridj": reverse_lazy('rp:index'), "uriname": "Home"},
            {"uridj": reverse_lazy('rp:personas'), "uriname": "Personas"},
            {"uridj": reverse_lazy('rp:registropersonas'), "uriname": "Registro"}
        ]
        context['url_create'] = reverse_lazy('rp:registropersonas')
        context['url_list'] = reverse_lazy('rp:personas')
        context['action'] = 'add'
        return context

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                data = form.save()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)