from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView

from core.base.mixins import ValidatePermissionRequiredMixin
from core.representantetecnico.mixins import IsTechnicalRepresentative
from core.representantetecnico.models import Proveedor


class EmpresaListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    permission_required = ('representantetecnico.view_proveedor',)
    model = Proveedor
    template_name = "empresa/list.html"

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Proveedor.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data["error"] = str(e)
        return JsonResponse(data, safe=False)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usertitle'] = "Representante Técnico"
        context['title'] = "Empresas registradas"
        context['icontitle'] = "store-alt"
        context['urls'] = [
            {"uridj": reverse_lazy('dashboard'), "uriname": "Home"},
            {"uridj": reverse_lazy('rp:empresas'), "uriname": "Empresas"}
        ]
        context['create_url'] = reverse_lazy('rp:registroempresa')
        return context
