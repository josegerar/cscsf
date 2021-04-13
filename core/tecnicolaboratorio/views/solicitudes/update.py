import json

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from app.settings import LOGIN_REDIRECT_URL
from core.base.mixins import ValidatePermissionRequiredMixin, PassRequestToFormViewMixin
from core.representantetecnico.models import Solicitud, EstadoTransaccion, SolicitudDetalle
from core.tecnicolaboratorio.forms.formSolicitud import SolicitudForm


class SolicitudUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin,
                          PassRequestToFormViewMixin, UpdateView):
    permission_required = ('representantetecnico.change_solicitud',)
    model = Solicitud
    form_class = SolicitudForm
    template_name = 'solicitudtl/create.html'
    success_url = reverse_lazy('tl:solicitudes')
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object is not None:
            if self.object.estado_solicitud is not None:
                if self.object.estado_solicitud.estado in ['almacenado', 'entregado', 'aprobado', 'recibido']:
                    messages.error(request, 'Solicitud de entrega de sustancia ya fue aprobada')
                    messages.error(request, 'No es posible actualizar')
                    messages.error(request, 'Pongase en contacto con el administrador del sistema')
                    return HttpResponseRedirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Actualizar solicitud"
        context['icontitle'] = "edit"
        context['url_list'] = self.success_url
        context['action'] = 'edit'
        context['urls'] = [
            {"uridj": LOGIN_REDIRECT_URL, "uriname": "Home"},
            {"uridj": self.success_url, "uriname": "Solicitudes"},
            {"uridj": reverse_lazy('tl:actualizacionsolicitud'), "uriname": "Edicción"}
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
                        solicitud = form.instance
                        detalle_solicitud_new = json.loads(request.POST['detalle_solicitud'])
                        self.update_informe(solicitud, detalle_solicitud_new)
                    else:
                        data['error'] = form.errors
                else:
                    data['error'] = 'ha ocurrido un error'
            else:
                data['error'] = 'ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def update_informe(self, solicitud, detalle_solicitud_new):
        with transaction.atomic():
            estadosolicitud = EstadoTransaccion.objects.get(estado='registrado')
            if solicitud.estado_solicitud.estado in ['almacenado', 'entregado', 'aprobado',
                                                     'recibido']:
                raise Exception("No es posible actualizar este registro")

            solicitud.estado_solicitud_id = estadosolicitud.id
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
                sustancia_new = dc_new['sustancia']

                for dc_old in detalle_solicitud_old:
                    if dc_old.id == dc_new['id']:
                        exits_old = True
                        item_det_new = dc_old
                        break

                if exits_old is False and item_det_new is None:
                    item_det_new = SolicitudDetalle()

                item_det_new.sustancia_id = sustancia_new['id']
                item_det_new.solicitud_id = solicitud.id
                item_det_new.cantidad_solicitada = float(dc_new['cantidad_solicitud'])
                item_det_new.save()
