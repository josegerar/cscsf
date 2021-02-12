from django.contrib.auth import logout
from django.views.generic import RedirectView


class LogoutRedirectView(RedirectView):
    pattern_name = 'session:login'

    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return super().dispatch(request, *args, **kwargs)
