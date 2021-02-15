from django.shortcuts import redirect


class IsTechnicalRepresentative(object):

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_representative:
            return super().dispatch(request, *args, **kwargs)
        return redirect('session:login')
