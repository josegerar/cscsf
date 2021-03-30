from django.shortcuts import render
from django.views.generic import TemplateView
from django.templatetags.static import static


class IndexView(TemplateView):
    template_name = "indexhome.html"


def list_view(request):
    # dictionary for initial data with
    # field names as keys
    context = {"name": "Kevin Jordan", "username": "kchevesc", "email": "kchevesc2012@uteq.edu.ec",
               "urllogin": request.build_absolute_uri("/"),
               "logo": request.build_absolute_uri(static('img/uteq/logoUTEQoriginal1.png'))}
    return render(request, "correo/correo.html", context)
