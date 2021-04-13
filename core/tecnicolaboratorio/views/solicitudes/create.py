import json

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from app.settings import LOGIN_REDIRECT_URL
from core.base.mixins import ValidatePermissionRequiredMixin, PassRequestToFormViewMixin
from core.representantetecnico.models import Solicitud, EstadoTransaccion, SolicitudDetalle
from core.tecnicolaboratorio.forms.formSolicitud import SolicitudForm
from core.tecnicolaboratorio.models import Laboratorio


class SolicitudCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin,
                          PassRequestToFormViewMixin, CreateView):
    permission_required = ('representantetecnico.add_solicitud',)
    model = Solicitud
    form_class = SolicitudForm
    template_name = "solicitudtl/create.html"
    success_url = reverse_lazy("tl:solicitudes")
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        if Laboratorio.objects.filter(responsable_id=request.user.id).exists() is False:
            messages.error(request, 'Aun no tiene laboratorios asignados a este usuario')
            return HttpResponseRedirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Registro solicitudes de entrega sustancias"
        context['icontitle'] = "plus"
        context['url_list'] = self.success_url
        context['action'] = 'add'
        context['urls'] = [
            {"uridj": LOGIN_REDIRECT_URL, "uriname": "Home"},
            {"uridj": self.success_url, "uriname": "Solicitudes"},
            {"uridj": reverse_lazy('tl:registrosolicitud'), "uriname": "Registro"}
        ]
        return context

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST.get('action')
            if action is not None:
                if action == 'add':
                    form = self.get_form()
                    if form.is_valid():
                        solicitud = form.instance
                        sustancias = json.loads(request.POST['sustancias'])
                        self.create_solicitud(solicitud, sustancias, request.user)
                    else:
                        data['error'] = form.errors
                else:
                    data['error'] = 'Ha ocurrido un error'
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def create_solicitud(self, solicitud, sustancias, user):
        estadosolicitud = EstadoTransaccion.objects.get(estado='registrado')
        with transaction.atomic():
            solicitud.estado_solicitud_id = estadosolicitud.id
            solicitud.solicitante_id = user.id
            solicitud.save()

            for i in sustancias:
                det = SolicitudDetalle()
                det.sustancia_id = i['id']
                det.solicitud_id = solicitud.id
                det.cantidad_solicitada = float(i['cantidad_solicitud'])
                det.save()
