from django.urls import path

from CSSF.views import myfirstview, mysecondview, mainIndex, bodIndex, labIndex

app_name = "cssf"

urlpatterns = [
    path('index/', mainIndex, name="index"),
    path('indexBod/', bodIndex, name="indexBod"),
    path('indexLab/', labIndex, name="indexLab"),
    path('uno/', myfirstview, name="vista1"),
    path('dos/', mysecondview, name="vista2")
]