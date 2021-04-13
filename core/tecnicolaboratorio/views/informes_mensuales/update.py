import json

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from app.settings import LOGIN_REDIRECT_URL
from core.base.mixins import ValidatePermissionRequiredMixin, PassRequestToFormViewMixin
from core.representantetecnico.models import EstadoTransaccion, InformesMensuales, InformesMensualesDetalle
from core.tecnicolaboratorio.forms.formInformeMensual import InformeMensualForm


class InformesMensualesUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin,
                                  PassRequestToFormViewMixin, UpdateView):
    permission_required = ('representantetecnico.change_informesmensuales',)
    model = InformesMensuales
    form_class = InformeMensualForm
    template_name = "informesmensuales/create.html"
    success_url = reverse_lazy("tl:informesmensuales")
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object is not None:
            if self.object.estado_informe is not None:
                if self.object.estado_informe.estado == "archivado":
                    messages.error(request, 'Informe mensuales ya paso la fecha limite para editar')
                    messages.error(request, 'No es posible su eliminación')
                    messages.error(request, 'Pongase en contacto con el administrador del sistema')
                    return HttpResponseRedirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Actualizar informe mensual"
        context['icontitle'] = "edit"
        context['url_list'] = self.success_url
        context['action'] = 'edit'
        context['urls'] = [
            {"uridj": LOGIN_REDIRECT_URL, "uriname": "Home"},
            {"uridj": self.success_url, "uriname": "Informes mensuales"},
            {"uridj": reverse_lazy('tl:actualizacioninformesmensuales'), "uriname": "Edicción"}
        ]
        return context

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST.get('action')
            if action is not None:
                if action == 'edit':
                    form = self.get_form()
                    if form.is_valid():
                        informe_mensual = form.instance
                        self.verify_form_informe_updated(informe_mensual)
                        detalle_informe_new = json.loads(request.POST['detalle_informe'])
                        self.update_informe(informe_mensual, detalle_informe_new, request.user)
                    else:
                        data['error'] = form.errors
                else:
                    data['error'] = 'ha ocurrido un error'
            else:
                data['error'] = 'ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def verify_form_informe_updated(self, informe_new):
        informe_old = InformesMensuales.objects.get(pk=informe_new.id)
        if informe_old.laboratorio_id != informe_new.laboratorio_id:
            raise Exception('No se puede actualizar un laboratorio diferente')
        if informe_old.mes.id != informe_new.mes.id:
            raise Exception("No se puede actualizar a un mes diferente")
        if informe_old.year != informe_new.year:
            raise Exception("No se puede actualizar a un año diferente")

    def update_informe(self, informe_mensual, detalle_informe_new, user):
        estadoinforme = EstadoTransaccion.objects.get(estado='registrado')
        with transaction.atomic():
            if informe_mensual.estado_informe.estado == "archivado":
                raise Exception('No es posible actualizar este registro')
            informe_mensual.estado_informe_id = estadoinforme.id
            informe_mensual.laboratorista_id = user.id
            informe_mensual.save()
            detalle_informe_old = InformesMensualesDetalle.objects.filter(
                informe_id=informe_mensual.id)

            for dc_old in detalle_informe_old:
                exits_old = False
                for dc_new in detalle_informe_new:
                    if dc_old.id == dc_new['id']:
                        exits_old = True
                        break
                if exits_old is False:
                    dc_old.delete()

            detalle_informe_old = InformesMensualesDetalle.objects.filter(
                informe_id=informe_mensual.id)

            for dc_new in detalle_informe_new:
                exits_old = False
                item_det_new = None
                stock_new = dc_new['stock']

                for dc_old in detalle_informe_old:
                    if dc_old.id == dc_new['id']:
                        exits_old = True
                        item_det_new = dc_old
                        break

                if exits_old is False and item_det_new is None:
                    item_det_new = InformesMensualesDetalle()

                item_det_new.stock_id = stock_new['id']
                item_det_new.informe_id = informe_mensual.id
                item_det_new.cantidad = float(dc_new['cantidad'])
                item_det_new.save()
