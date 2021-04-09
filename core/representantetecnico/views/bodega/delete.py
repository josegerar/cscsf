from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import DeleteView

from app.settings import LOGIN_REDIRECT_URL
from core.base.mixins import ValidatePermissionRequiredMixin
from core.bodega.models import Bodega
from core.representantetecnico.models import Stock, Solicitud, ComprasPublicas


class BodegaDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    permission_required = ('bodega.delete_bodega',)
    model = Bodega
    template_name = 'delete.html'
    success_url = reverse_lazy('rp:bodegas')
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if Stock.objects.filter(bodega_id=self.object.id).exists() or Solicitud.objects.filter(
                bodega_id=self.object.id).exists() or ComprasPublicas.objects.filter(bodega_id=self.object.id).exists():
            messages.error(request, 'Bodega ya posee stock registrado')
            messages.error(request, 'No es posible su eliminación')
            messages.error(request, 'Pongase en contacto con el administrador del sistema')
            return HttpResponseRedirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            if Stock.objects.filter(bodega_id=self.object.id).exists() or Solicitud.objects.filter(
                    bodega_id=self.object.id).exists() or ComprasPublicas.objects.filter(
                bodega_id=self.object.id).exists():
                raise Exception("No es posible eliminar este registro")
            self.object.delete()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Eliminar bodega"
        context['icontitle'] = "trash-alt"
        context['url_list'] = self.success_url
        context['urls'] = [
            {"uridj": LOGIN_REDIRECT_URL, "uriname": "Home"},
            {"uridj": self.success_url, "uriname": "Bodegas"},
            {"uridj": reverse_lazy('rp:eliminarbodega'), "uriname": "Eliminar"}
        ]
        return context
