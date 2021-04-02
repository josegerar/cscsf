from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView

from app.settings import LOGIN_REDIRECT_URL
from core.base.mixins import ValidatePermissionRequiredMixin
from core.login.models import User
from core.representantetecnico.models import Persona


class PersonaListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    permission_required = ('login.view_persona',)
    model = Persona
    template_name = "personas/list.html"

    def get(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.GET.get('action')
            if action is not None:
                if action == 'searchdata':
                    data = []
                    type_data = request.GET.get('type')
                    id_data = request.GET.get('id')
                    if type_data == 'lab':
                        query = Persona.objects.filter(user_creation_id=request.user.id)
                    else:
                        query = Persona.objects.all()
                    for per in query:
                        item = {'id': per.id, 'nombre': per.nombre, 'apellido': per.apellido, 'cedula': per.cedula,
                                'is_del': True}
                        if User.objects.filter(persona_id=per.id).exists():
                            item["is_del"] = False
                        data.append(item)
                    return JsonResponse(data, safe=False)
        except Exception as e:
            data['error'] = str(e)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Investigadores / Docentes"
        context['icontitle'] = "user-friends"
        context['create_url'] = reverse_lazy('rp:registropersonas')
        context['urls'] = [
            {"uridj": LOGIN_REDIRECT_URL, "uriname": "Home"},
            {"uridj": reverse_lazy('rp:personas'), "uriname": "Investigadores"}
        ]
        return context
