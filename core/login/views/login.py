from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.urls import reverse_lazy


class LoginFormView(LoginView):
    template_name = "login.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Iniciar sessión"
        return context

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return self.redirect_rols()
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        login(self.request, form.get_user())
        return self.redirect_rols()

    def redirect_rols(self):
        if self.request.user.is_superuser:
            return HttpResponseRedirect('/admin/')
        if self.request.user.is_grocer:
            return HttpResponseRedirect(reverse_lazy('bdg:index'))
        elif self.request.user.is_representative:
            return HttpResponseRedirect(reverse_lazy('rp:index'))
        elif self.request.user.is_laboratory_worker:
            return HttpResponseRedirect(reverse_lazy('tl:index'))
        else:
            logout(self.request)
            return HttpResponseNotFound('<h1>Usuario ingresado no pertenece a ningun rol de usuario</h1>')
