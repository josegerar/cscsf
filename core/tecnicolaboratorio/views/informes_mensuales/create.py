import json

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from app.settings import LOGIN_REDIRECT_URL
from core.base.mixins import ValidatePermissionRequiredMixin, PassRequestToFormViewMixin
from core.representantetecnico.models import InformesMensuales, InformesMensualesDetalle
from core.tecnicolaboratorio.forms.formInformeMensual import InformeMensualForm


class InformesMensualesCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin,
                                  PassRequestToFormViewMixin, CreateView):
    permission_required = ('representantetecnico.add_informesmensuales',)
    model = InformesMensuales
    form_class = InformeMensualForm
    template_name = "informesmensuales/create.html"
    success_url = reverse_lazy("tl:informesmensuales")
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        if InformesMensuales.objects.filter(is_editable=True).exists():
            messages.error(request, 'Aun existen informes por archivar')
            messages.error(request, 'Debe archivar todos los informes antes de crear otro')
            messages.error(request, 'Pongase en contacto con el administrador del sistema')
            return HttpResponseRedirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Registro informes mensuales de laboratorio"
        context['icontitle'] = "plus"
        context['url_list'] = self.success_url
        context['action'] = 'add'
        context['urls'] = [
            {"uridj": LOGIN_REDIRECT_URL, "uriname": "Home"},
            {"uridj": self.success_url, "uriname": "Solicitudes"},
            {"uridj": reverse_lazy('tl:registroinformesmensuales'), "uriname": "Registro"}
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
                        informe = form.instance
                        if informe is not None:
                            with transaction.atomic():
                                if InformesMensuales.verify_month_exist_with_year(informe.mes.id, informe.year,
                                                                                  informe.laboratorio.id):
                                    raise Exception(
                                        'Ya existe un informe registrado con este mes para este año con el '
                                        'laboratorio {}'.format(informe.laboratorio.nombre)
                                    )
                                sustancias = json.loads(request.POST['sustancias'])
                                informe.laboratorista_id = request.user.id
                                informe.save()

                                for i in sustancias:
                                    det = InformesMensualesDetalle()
                                    det.stock_id = i['id']
                                    det.informe_id = informe.id
                                    det.cantidad = float(i['cantidad_consumida'])
                                    det.save()
                                data["id"] = informe.id
                                data["url"] = reverse_lazy('tl:actualizacioninformesmensuales',
                                                           kwargs={'pk': informe.id})
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
