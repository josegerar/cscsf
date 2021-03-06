from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView

from app.settings import LOGIN_REDIRECT_URL
from core.base.mixins import ValidatePermissionRequiredMixin
from core.bodega.models import Bodega


class BodegaListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    permission_required = ('bodega.view_bodega',)
    model = Bodega
    template_name = "bodega/list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Bodegas registradas"
        context['icontitle'] = "store-alt"
        context['create_url'] = reverse_lazy('rp:registrobodega')
        context['urls'] = [
            {"uridj": LOGIN_REDIRECT_URL, "uriname": "Home"},
            {"uridj": reverse_lazy('rp:bodegas'), "uriname": "Bodegas"}
        ]
        return context

    def get(self, request, *args, **kwargs):
        try:
            action = request.GET.get('action')
            if action is not None:
                if action == 'searchdata':
                    data = self.search_data(request.user)
                    return JsonResponse(data, safe=False)
        except Exception as e:
            messages.error(request, str(e))
        return super().get(request, *args, **kwargs)

    def search_data(self, user):
        if user.is_grocer:
            query = Bodega.objects.filter(responsable_id=user.id)
        else:
            query = Bodega.objects.all()
        data = []
        for i in query:
            item = {'id': i.id, 'nombre': i.nombre, 'responsable': '', 'is_del': True, 'dir': i.direccion}
            if i.responsable is not None:
                item['responsable'] = i.responsable.get_user_info()
            if i.stock_set.all().exists():
                item['is_del'] = False
            data.append(item)
        return data
