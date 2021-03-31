from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib import messages


class IsUserUCSCSF(object):

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_representative or request.user.is_grocer or request.user.is_laboratory_worker:
            return super().dispatch(request, *args, **kwargs)
        logout(request)
        messages.error(request, 'Usuario no tiene permiso para entrar al sistema')
        messages.error(request, 'Pongase en contacto con el administrador del sistema')
        return redirect('session:login')


class ValidatePermissionRequiredMixin(object):
    permission_required = ''
    url_redirect = None

    def get_perms(self):
        if isinstance(self.permission_required, str):
            perms = (self.permission_required,)
        else:
            perms = self.permission_required
        return perms

    def get_url_redirect(self):
        if self.url_redirect is None:
            return reverse_lazy('session:login')
        else:
            return self.url_redirect

    def dispatch(self, request, *args, **kwargs):
        if request.user.has_perms(self.get_perms()):
            if request.user.is_pass_update:
                if request.user.persona is not None:
                    if request.user.persona.is_info_update:
                        return super().dispatch(request, *args, **kwargs)
                messages.error(request, 'No ha actualizado su información')
            else:
                messages.error(request, 'No tiene permiso de ingresar al sistema, cambie su contraseña inicial')
        else:
            messages.error(request, 'No tiene permiso para entrar a este módulo')
            messages.error(request, 'Pongase en contacto con el administrador del sistema')
        return HttpResponseRedirect(self.get_url_redirect())


class PassRequestToFormViewMixin:
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs
