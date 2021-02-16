from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView

from core.base.mixins import ValidatePermissionRequiredMixin
from core.representantetecnico.models import ComprasPublicas, Laboratorio


class ComprasListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    permission_required = ('representantetecnico.view_compraspublicas', 'tecnicolaboratorio.view_laboratorio',)
    model = ComprasPublicas
    template_name = "compras/list.html"

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in ComprasPublicas.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data["error"] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usertitle'] = "Representante Técnico"
        context['title'] = "Compras registradas"
        context['icontitle'] = "store-alt"
        context['laboratorios'] = Laboratorio.objects.all()
        context['create_url'] = reverse_lazy('rp:registrocompras')
        context['urls'] = [
            {"uridj": reverse_lazy('dashboard'), "uriname": "Home"},
            {"uridj": reverse_lazy('rp:compras'), "uriname": "Compras"}
        ]
        return context
