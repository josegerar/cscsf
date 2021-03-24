from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from app.settings import LOGIN_REDIRECT_URL
from core.base.mixins import ValidatePermissionRequiredMixin
from core.bodega.models import Sustancia, Bodega, Stock
from core.representantetecnico.forms.formSustancia import SustanciaForm
from core.tecnicolaboratorio.models import Laboratorio


class SustanciaUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    permission_required = ('bodega.change_sustancia',)
    model = Sustancia
    form_class = SustanciaForm
    template_name = 'sustancia/create.html'
    success_url = reverse_lazy('rp:sustancias')
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usertitle'] = "Representante Técnico"
        context['title'] = "Actualizar sustancia"
        context['icontitle'] = "edit"
        context['url_list'] = self.success_url
        context['action'] = 'edit'
        context['urls'] = [
            {"uridj": LOGIN_REDIRECT_URL, "uriname": "Home"},
            {"uridj": self.success_url, "uriname": "Sustancia"},
            {"uridj": reverse_lazy('rp:actualizacionsustancia'), "uriname": "Edicción"}
        ]
        return context

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST.get('action')
            if action is not None:
                if action == 'edit':
                    form = self.get_form()
                    data = form.save()

                elif action == 'list_desglose':
                    data = []
                    desgloses = Stock.objects.filter(sustancia_id=self.object.id, )
                    for i in Bodega.objects.all().order_by('nombre'):
                        item = i.toJSON()
                        item['tipo'] = 'bodega'
                        item['cantidad_ingreso'] = 0.0000
                        data.append(item)
                    for i in Laboratorio.objects.all().order_by('nombre'):
                        item = i.toJSON()
                        item['tipo'] = 'laboratorio'
                        item['cantidad_ingreso'] = 0.0000
                        data.append(item)
                else:
                    data['error'] = "Ha ocurrido un error"
            else:
                data['error'] = "Ha ocurrido un error"
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)
