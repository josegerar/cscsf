from django.urls import path

from CSSF.usviews.views_rp import mainIndex

urlpatterns = [
    path('index/', mainIndex, name="index"),
]