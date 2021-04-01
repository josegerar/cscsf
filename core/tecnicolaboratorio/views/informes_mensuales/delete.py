from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import DeleteView

from app.settings import LOGIN_REDIRECT_URL
from core.base.mixins import ValidatePermissionRequiredMixin
from core.representantetecnico.models import InformesMensuales


class InformesMensualesDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    permission_required = ('representantetecnico.delete_informesmensuales',)
    model = InformesMensuales
    template_name = 'delete.html'
    success_url = reverse_lazy('tl:informesmensuales')
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object is not None:
            if self.object.is_editable is False:
                messages.error(request, 'Informe mensuales ya paso la fecha limite para editar')
                messages.error(request, 'No es posible su eliminación')
                messages.error(request, 'Pongase en contacto con el administrador del sistema')
                return HttpResponseRedirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            with transaction.atomic():
                informe = self.object
                for det in informe.informesmensualesdetalle_set.all():
                    for desglose_det in det.desgloseinfomemensualdetalle_set.all():
                        solicitud_detalle = desglose_det.solicitud_detalle
                        solicitud_detalle.cantidad_consumida = solicitud_detalle.cantidad_consumida - desglose_det.cantidad
                        solicitud_detalle.save()
                informe.delete()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Eliminar informe mensual"
        context['icontitle'] = "trash-alt"
        context['url_list'] = self.success_url
        context['urls'] = [
            {"uridj": LOGIN_REDIRECT_URL, "uriname": "Home"},
            {"uridj": self.success_url, "uriname": "Informes mensuales"},
            {"uridj": reverse_lazy('tl:eliminarinformesmensuales'), "uriname": "Eliminar"}
        ]
        return context
