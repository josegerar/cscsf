from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import DeleteView

from core.base.mixins import ValidatePermissionRequiredMixin
from core.representantetecnico.models import DesgloseInfomeMensualDetalle, SolicitudDetalle


class DesgloseSustanciaInformeMensualDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    permission_required = ('representantetecnico.delete_desgloseinfomemensualdetalle',)
    model = DesgloseInfomeMensualDetalle
    template_name = 'desglosesustanciainformemensual/delete.html'
    success_url = reverse_lazy('tl:informesmensuales')
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object is not None:
            if self.object.informe_mensual_detalle is not None:
                if self.object.informe_mensual_detalle.informe is not None:
                    if self.object.informe_mensual_detalle.informe.is_editable is False:
                        messages.error(request, 'Informe actual ya esta cerrado')
                        messages.error(request, 'No es posible realizar operaciones sobre el mismo')
                        messages.error(request, 'Pongase en contacto con el administrador del sistema')
                        return HttpResponseRedirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            with transaction.atomic():
                desglose_informe_sustancia_detalle = self.object
                if desglose_informe_sustancia_detalle is None:
                    raise Exception(
                        "Registro inexistente"
                    )
                solicitud_detalle = desglose_informe_sustancia_detalle.solicitud_detalle
                solicitud_detalle.cantidad_consumida = solicitud_detalle.cantidad_consumida - desglose_informe_sustancia_detalle.cantidad
                solicitud_detalle.save()
                desglose_informe_sustancia_detalle.delete()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)
