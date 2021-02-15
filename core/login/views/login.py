from django.conf import settings
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect


class LoginFormView(LoginView):
    template_name = "login.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL)
        return super().dispatch(request, *args, **kwargs)
