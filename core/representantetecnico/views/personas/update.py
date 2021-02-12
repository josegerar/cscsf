from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView

from core.representantetecnico.forms.formPersona import PersonaForm
from core.representantetecnico.models import Persona


class PersonasUpdateView(UpdateView):
    model = Persona
    form_class = PersonaForm
    template_name = 'personas/create.html'
    success_url = reverse_lazy('rp:personas')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usertitle'] = "Representante Técnico"
        context['title'] = "Actualizar personas"
        context['icontitle'] = "edit"
        context['urls'] = [
            {"uridj": reverse_lazy('rp:index'), "uriname": "Home"},
            {"uridj": reverse_lazy('rp:personas'), "uriname": "Personas"},
            {"uridj": reverse_lazy('rp:registropersonas'), "uriname": "Registro"}
        ]
        context['url_list'] = reverse_lazy('rp:personas')
        context['action'] = 'edit'
        return context

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()
                data = form.save()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)