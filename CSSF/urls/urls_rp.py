from django.urls import path

from CSSF.views.rp.views_rp import mainIndex

app_name = "rp"

urlpatterns = [
    path('index/', mainIndex, name="index"),
]