from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView

from app.settings import LOGIN_REDIRECT_URL
from core.base.mixins import ValidatePermissionRequiredMixin
from core.login.models import User
from core.representantetecnico.models import Persona, Solicitud


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
                    if type_data == 'lab':
                        query = Persona.objects.filter(user_creation_id=request.user.id)
                    else:
                        query = Persona.objects.all()
                    for per in query:
                        item = {'id': per.id, 'nombre': per.nombre, 'apellido': per.apellido, 'cedula': per.cedula,
                                'is_del': True}
                        if User.objects.filter(persona_id=per.id).exists() or Solicitud.objects.filter(
                                responsable_actividad_id=per.id).exists():
                            item["is_del"] = False
                        data.append(item)
                    return JsonResponse(data, safe=False)
                elif action == 'search_user_person':
                    data = []
                    person_id = request.GET.get('person_id')
                    for user in User.objects.filter(persona_id=person_id):
                        data.append({'id': user.id, 'email': user.email, 'is_act': user.is_active,
                                     'is_rep': user.is_representative, 'is_lab': user.is_laboratory_worker,
                                     'is_groc': user.is_grocer})
                    return JsonResponse(data, safe=False)
        except Exception as e:
            data['error'] = str(e)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['icontitle'] = "user-friends"
        context['create_url'] = reverse_lazy('rp:registropersonas')
        context['urls'] = [
            {"uridj": LOGIN_REDIRECT_URL, "uriname": "Home"}
        ]
        if self.request.user.is_representative:
            context['title'] = "Personas"
            context['urls'].append({"uridj": reverse_lazy('rp:personas'), "uriname": "Personas"})
        elif self.request.user.is_laboratory_worker:
            context['title'] = "Investigadores / Docentes"
            context['urls'].append({"uridj": reverse_lazy('rp:personas'), "uriname": "Investigadores"})
        return context
