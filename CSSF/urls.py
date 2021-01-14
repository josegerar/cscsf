from django.urls import path

from CSSF.views import myfirstview, mysecondview, mainIndex

app_name = "cssf"

urlpatterns = [
    path('index/', mainIndex, name="index"),
    path('uno/', myfirstview, name="vista1"),
    path('dos/', mysecondview, name="vista2")
]