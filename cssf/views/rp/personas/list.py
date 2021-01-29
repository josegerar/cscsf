from django.urls import reverse_lazy
from django.views.generic import ListView

from cssf.models import Persona

class PersonaListView(ListView):
    model = Persona
    template_name = "rp/personas/list.html"

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Persona.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usertitle'] = "Representante Técnico"
        context['title'] = "Personas externas registradas"
        context['icontitle'] = "store-alt"
        context['urls'] = [
            {"uridj": reverse_lazy('rp:index'), "uriname": "Home"},
            {"uridj": reverse_lazy('rp:personas'), "uriname": "Personas"}
        ]
        context['create_url'] = reverse_lazy('rp:registropersonas')
        return context