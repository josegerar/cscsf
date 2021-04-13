from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from core.base.mixins import ValidatePermissionRequiredMixin
from core.representantetecnico.models import Sustancia, Stock


class SustanciaView(LoginRequiredMixin, ValidatePermissionRequiredMixin, TemplateView):
    permission_required = ('representantetecnico.view_sustancia',)
    template_name = 'sustancia/view.html'
    url_redirect = reverse_lazy('rp:sustancias')

    def dispatch(self, request, *args, **kwargs):
        try:
            self.object = Sustancia.objects.get(pk=kwargs['pk'])
            return super().dispatch(request, *args, **kwargs)
        except Exception as e:
            messages.error(request, str(e))
        return HttpResponseRedirect(self.url_redirect)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url_list'] = self.url_redirect
        context['icontitle'] = 'eye'
        context['title'] = '{} {}'.format("Sustancia", self.object.id)
        return context

    def get(self, request, *args, **kwargs):
        try:
            action = request.GET.get('action')
            if action is not None:
                if action == 'search_stock':
                    data = self.search_stock(request.user)
                    return JsonResponse(data, safe=False)
        except Exception as e:
            messages.error(request, str(e))
        return super().get(request, *args, **kwargs)

    def search_stock(self, user):
        data = []
        if user.is_laboratory_worker:
            query = Stock.objects.filter(laboratorio__responsable_id=user.id, sustancia_id=self.object.id)
        elif user.is_grocer:
            query = Stock.objects.filter(bodega__responsable_id=user.id, sustancia_id=self.object.id)
        else:
            query = Stock.objects.filter(sustancia_id=self.object.id)
        for i in query:
            item = {'id': i.id, 'cantidad': i.cantidad, 'type': '', 'nombre': ''}
            if i.laboratorio is not None:
                item['type'] = 'laboratorio'
                item['nombre'] = i.laboratorio.nombre
            elif i.bodega is not None:
                item['type'] = 'bodega'
                item['nombre'] = i.bodega.nombre
            data.append(item)
        return data
