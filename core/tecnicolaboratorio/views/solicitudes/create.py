import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView

from app.settings import LOGIN_REDIRECT_URL
from core.base.mixins import ValidatePermissionRequiredMixin, PassRequestToFormViewMixin
from core.representantetecnico.models import Solicitud, EstadoTransaccion, SolicitudDetalle
from core.tecnicolaboratorio.forms.formSolicitud import SolicitudForm


class SolicitudCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin,
                          PassRequestToFormViewMixin, CreateView):
    permission_required = ('representantetecnico.add_solicitud',)
    model = Solicitud
    form_class = SolicitudForm
    template_name = "solicitudtl/create.html"
    success_url = reverse_lazy("tl:solicitudes")
    url_redirect = success_url

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usertitle'] = "Representante Técnico"
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
                        estadosolicitud = EstadoTransaccion.objects.get(estado='registrado')
                        if solicitud is not None and estadosolicitud is not None:
                            with transaction.atomic():
                                sustancias = json.loads(request.POST['sustancias'])
                                solicitud.estado_solicitud_id = estadosolicitud.id
                                solicitud.solicitante_id = request.user.id
                                solicitud.save()

                                for i in sustancias:
                                    stock_selected = i['stock_selected']
                                    det = SolicitudDetalle()
                                    det.stock_id = stock_selected['id']
                                    det.solicitud_id = solicitud.id
                                    det.cantidad = float(i['cantidad_solicitud'])
                                    det.save()
                        else:
                            data['error'] = 'Ha ocurrido un error'
                    else:
                        data['error'] = 'Ha ocurrido un error'
                else:
                    data['error'] = 'Ha ocurrido un error'
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)
