from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from core.base.mixins import IsUserUCSCSF
from core.login.models import User


class DashBoard(LoginRequiredMixin, IsUserUCSCSF, TemplateView):
    template_name = 'dashboard/dashboard.html'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST.get('action')
            if action is not None:
                if action == 'actChangePass':
                    pass1 = request.POST.get('pass')
                    pass2 = request.POST.get('pass2')
                    code = request.POST.get('codeConfirm')
                    if pass1 is not None and pass2 is not None and code is not None:
                        if pass1==pass2:
                            user = request.user
                            if code == user.codeconfirm:
                                user.codeconfirm = None
                            else:
                                data['error'] = 'código erroreo'
                        else:
                            data['error'] = 'Las contraseñas no coinciden'
                    else:
                        data['error'] = 'Datos incorrectos'
                else:
                    data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data["error"] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Dashboard"
        return context


