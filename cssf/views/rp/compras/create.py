from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView

from cssf.forms.rp.formCompra import ComprasForm
from cssf.models import ComprasPublicas, Laboratorio


class ComprasCreateView(CreateView):
    model = ComprasPublicas
    form_class = ComprasForm
    template_name = 'rp/compras/create.html'
    success_url = reverse_lazy('rp:compras')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usertitle'] = "Representante Técnico"
        context['title'] = "Registrar compra"
        context['icontitle'] = "plus"
        context['urls'] = [
            {"uridj": reverse_lazy('rp:index'), "uriname": "Home"},
            {"uridj": reverse_lazy('rp:compras'), "uriname": "Compras"},
            {"uridj": reverse_lazy('rp:registrocompras'), "uriname": "Registro"}
        ]
        context['url_create'] = reverse_lazy('rp:registrocompras')
        context['url_list'] = reverse_lazy('rp:compras')
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
