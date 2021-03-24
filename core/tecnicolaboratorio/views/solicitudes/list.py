from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView

from app.settings import LOGIN_REDIRECT_URL
from core.base.mixins import ValidatePermissionRequiredMixin
from core.representantetecnico.models import Solicitud


class SolicitudListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    permission_required = ('representantetecnico.view_solicitud',)
    model = Solicitud
    template_name = "solicitud/list.html"

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Solicitud.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data["error"] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usertitle'] = "Representante Técnico"
        context['title'] = "Solicitudes registradas"
        context['icontitle'] = "store-alt"
        context['create_url'] = reverse_lazy('tl:registrosolicitud')
        context['urls'] = [
            {"uridj": LOGIN_REDIRECT_URL, "uriname": "Home"},
            {"uridj": reverse_lazy('tl:solicitudes'), "uriname": "Solicitudes"}
        ]
        return context
