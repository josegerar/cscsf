from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView

from app.settings import LOGIN_REDIRECT_URL
from core.base.mixins import ValidatePermissionRequiredMixin
from core.tecnicolaboratorio.models import Laboratorio


class LaboratorioListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    permission_required = ('tecnicolaboratorio.view_laboratorio',)
    model = Laboratorio
    template_name = "laboratorio/list.html"

    def get(self, request, *args, **kwargs):
        try:
            action = request.GET.get('action')
            if action is not None:
                if action == 'searchdata':
                    data = self.search_data()
                    return JsonResponse(data, safe=False)
        except Exception as e:
            messages.error(request, str(e))
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Laboratorios registrados"
        context['icontitle'] = "store-alt"
        context['create_url'] = reverse_lazy('rp:registrolaboratorio')
        context['urls'] = [
            {"uridj": LOGIN_REDIRECT_URL, "uriname": "Home"},
            {"uridj": reverse_lazy('rp:laboratorios'), "uriname": "Laboratorios"}
        ]
        return context

    def search_data(self):
        data = []
        for i in Laboratorio.objects.all():
            item = {'id': i.id, 'nombre': i.nombre, 'responsable': '', 'is_del': True, 'dir': i.direccion}
            if i.responsable is not None:
                item['responsable'] = i.responsable.get_user_info()
            if i.stock_set.all().exists():
                item['is_del'] = False
            data.append(item)
        return data
