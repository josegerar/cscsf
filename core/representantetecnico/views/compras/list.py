from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView

from core.representantetecnico.models import ComprasPublicas, Laboratorio


class ComprasListView(ListView):
    model = ComprasPublicas
    template_name = "compras/list.html"

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            data = Laboratorio.objects.get(pk=request.POST['id']).toJSON()
        except Exception as e:
            data["error"] = str(e)
        return JsonResponse(data)

    def get_queryset(self):
        return ComprasPublicas.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usertitle'] = "Representante Técnico"
        context['title'] = "Compras registradas"
        context['icontitle'] = "store-alt"
        context['laboratorios'] = Laboratorio.objects.all()
        context['urls'] = [
            {"uridj": reverse_lazy('rp:index'), "uriname": "Home"},
            {"uridj": reverse_lazy('rp:compras'), "uriname": "Compras"}
        ]
        context['create_url'] = reverse_lazy('rp:registrocompras')
        return context
