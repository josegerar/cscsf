import json

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from app.settings import LOGIN_REDIRECT_URL
from core.base.mixins import ValidatePermissionRequiredMixin, PassRequestToFormViewMixin
from core.representantetecnico.models import Solicitud, EstadoTransaccion, SolicitudDetalle, InformesMensuales, \
    InformesMensualesDetalle
from core.tecnicolaboratorio.forms.formInformeMensual import InformeMensualForm
from core.tecnicolaboratorio.forms.formSolicitud import SolicitudForm


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
            if self.object.is_editable is False:
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

    def get(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.GET.get('action')
            if action is not None:
                if action == 'informe_detail':
                    data = []
                    informe_id = kwargs.get("pk")
                    for i in InformesMensualesDetalle.objects.filter(informe_id=informe_id):
                        data.append({
                            'id': i.id,
                            'sustancia': {'id': i.stock.sustancia.id, 'nombre': i.stock.sustancia.nombre},
                            'unidad_medida': i.stock.sustancia.unidad_medida.nombre,
                            'cantidad_consumida': i.cantidad,
                            'cantidad_lab': i.stock.cantidad
                        })
                    return JsonResponse(data, safe=False)
        except Exception as e:
            data['error'] = str(e)
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST.get('action')
            if action is not None:
                if action == 'edit':
                    form = self.get_form()
                    if form.is_valid():
                        solicitud = form.instance
                        estadosolicitud = EstadoTransaccion.objects.get(estado='registrado')
                        if solicitud is not None and estadosolicitud is not None:
                            with transaction.atomic():
                                detalle_solicitud_new = json.loads(request.POST['detalle_solicitud'])
                                solicitud.estado_solicitud_id = estadosolicitud.id
                                solicitud.observacion = ""
                                solicitud.save()
                                detalle_solicitud_old = SolicitudDetalle.objects.filter(solicitud_id=solicitud.id)

                                for dc_old in detalle_solicitud_old:
                                    exits_old = False
                                    for dc_new in detalle_solicitud_new:
                                        if dc_old.id == dc_new['id']:
                                            exits_old = True
                                            break
                                    if exits_old is False:
                                        dc_old.delete()

                                detalle_solicitud_old = SolicitudDetalle.objects.filter(solicitud_id=solicitud.id)

                                for dc_new in detalle_solicitud_new:
                                    exits_old = False
                                    item_det_new = None
                                    stock_old = dc_new['stock']
                                    sustancia_new = stock_old['sustancia']
                                    stock_selected = sustancia_new['stock_selected']

                                    for dc_old in detalle_solicitud_old:
                                        if dc_old.id == dc_new['id']:
                                            exits_old = True
                                            item_det_new = dc_old
                                            break

                                    if exits_old is False and item_det_new is None:
                                        item_det_new = SolicitudDetalle()

                                    item_det_new.stock_id = stock_selected['id']
                                    item_det_new.solicitud_id = solicitud.id
                                    item_det_new.cantidad = float(dc_new['cantidad'])
                                    item_det_new.save()

                        else:
                            data['error'] = 'ha ocurrido un error'
                    else:
                        data['error'] = 'ha ocurrido un error'

                elif action == 'searchdetail':
                    data = []
                    detalle_solicitud = SolicitudDetalle.objects.filter(solicitud_id=self.object.id)
                    for dci in detalle_solicitud:
                        data.append(dci.toJSON(ver_solicitud=False))
                else:
                    data['error'] = 'ha ocurrido un error'
            else:
                data['error'] = 'ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)
