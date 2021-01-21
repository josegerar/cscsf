from django.urls import path

from CSSF.usviews.views_tl import labIndex

urlpatterns = [
    path('index/', labIndex, name="indexLab")
]