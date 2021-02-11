from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import DeleteView

from core.representantetecnico.models import Persona


class PersonasDeleteView(DeleteView):
    model = Persona
    template_name = 'personas/delete.html'
    success_url = reverse_lazy('rp:personas')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return  super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usertitle'] = "Representante Técnico"
        context['title'] = "Eliminar personas"
        context['icontitle'] = "trash-alt"
        context['urls'] = [
            {"uridj": reverse_lazy('rp:index'), "uriname": "Home"},
            {"uridj": reverse_lazy('rp:personas'), "uriname": "Personas"},
            {"uridj": reverse_lazy('rp:registropersonas'), "uriname": "Registro"}
        ]
        context['url_list'] = reverse_lazy('rp:personas')
        return context