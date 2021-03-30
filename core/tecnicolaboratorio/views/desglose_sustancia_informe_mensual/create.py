from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView

from core.base.mixins import ValidatePermissionRequiredMixin
from core.representantetecnico.models import DesgloseInfomeMensualDetalle, SolicitudDetalle
from core.tecnicolaboratorio.forms.formDesgloseSustanciaInformeMensual import DesgloseSustanciaInformeMensualForm


class DesgloseSustanciaInformeMensualCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin,
                                                CreateView):
    permission_required = ('representantetecnico.add_desgloseinfomemensualdetalle',)
    model = DesgloseInfomeMensualDetalle
    form_class = DesgloseSustanciaInformeMensualForm
    template_name = "desglosesustanciainformemensual/create.html"
    success_url = reverse_lazy("tl:informesmensuales")
    url_redirect = success_url

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST.get('action')
            if action is not None:
                if action == 'add':
                    form = self.get_form()
                    if form.is_valid():
                        desglose_sustancia_informe_mensual = form.instance
                        id_detalle = int(request.POST.get('id_detalle'))
                        if desglose_sustancia_informe_mensual is not None and id_detalle is not None:
                            with transaction.atomic():
                                if desglose_sustancia_informe_mensual.cantidad <= 0:
                                    raise Exception('Debe ingresar una cantidad de cosumo valida')
                                solicitud_detalle = SolicitudDetalle.objects.get(
                                    id=desglose_sustancia_informe_mensual.solicitud_detalle_id)
                                if solicitud_detalle is None:
                                    raise Exception("Error en los datos")
                                solicitud_detalle.cantidad_consumida = solicitud_detalle.cantidad_consumida + desglose_sustancia_informe_mensual.cantidad
                                desglose_sustancia_informe_mensual.informe_mensual_detalle_id = id_detalle
                                desglose_sustancia_informe_mensual.save()
                                solicitud_detalle.save()
                        else:
                            data['error'] = 'Ha ocurrido un error1'
                    else:
                        data['error'] = form.errors
                else:
                    data['error'] = 'Ha ocurrido un error3'
            else:
                data['error'] = 'Ha ocurrido un error4'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)
