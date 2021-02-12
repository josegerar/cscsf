from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView

from core.representantetecnico.models import Proveedor


class EmpresaListView(ListView):
    model = Proveedor
    template_name = "empresa/list.html"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Proveedor.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usertitle'] = "Representante Técnico"
        context['title'] = "Empresas registradas"
        context['icontitle'] = "store-alt"
        context['urls'] = [
            {"uridj": reverse_lazy('rp:index'), "uriname": "Home"},
            {"uridj": reverse_lazy('rp:empresas'), "uriname": "Empresas"}
        ]
        context['create_url'] = reverse_lazy('rp:registroempresa')
        return context