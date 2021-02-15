from django.contrib.auth import logout
from django.shortcuts import redirect


class IsUserUCSCSF(object):

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_representative or request.user.is_grocer or request.user.is_laboratory_worker:
            return super().dispatch(request, *args, **kwargs)
        logout(request)
        return redirect('session:login')
