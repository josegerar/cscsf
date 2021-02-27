from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView

from app.settings import LOGIN_REDIRECT_URL
from core.base.mixins import ValidatePermissionRequiredMixin
from core.bodega.models import Sustancia, Bodega
from core.representantetecnico.forms.formSustancia import SustanciaForm
from core.tecnicolaboratorio.models import Laboratorio


class SustanciaCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    permission_required = ('bodega.add_sustancia',)
    model = Sustancia
    form_class = SustanciaForm
    template_name = "sustancia/create.html"
    success_url = reverse_lazy("rp:sustancias")
    url_redirect = success_url

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usertitle'] = "Representante Técnico"
        context['title'] = "Registro sustancias"
        context['icontitle'] = "plus"
        context['url_list'] = self.success_url
        context['action'] = 'add'
        context['urls'] = [
            {"uridj": LOGIN_REDIRECT_URL, "uriname": "Home"},
            {"uridj": self.success_url, "uriname": "Sustancias"},
            {"uridj": reverse_lazy('rp:registrosustancias'), "uriname": "Registro"}
        ]
        return context

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                data = form.save()
            elif action == 'list_desglose':
                data = []
                for i in Bodega.objects.all():
                    item = i.toJSON()
                    item['tipo'] = 'bodega'
                    item['cantidad_ingreso'] = 0.0000
                    data.append(item)
                for i in Laboratorio.objects.all():
                    item = i.toJSON()
                    item['tipo'] = 'laboratorio'
                    item['cantidad_ingreso'] = 0.0000
                    data.append(item)
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)
