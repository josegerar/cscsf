from django.urls import path

from cssf.views.tl.views_tl import labIndex

app_name = "tl"

urlpatterns = [
    path('index/', labIndex, name="index")
]