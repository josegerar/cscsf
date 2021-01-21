from django.urls import path

from CSSF.views.bdg.views_bdg import bodIndex

app_name = "bdg"

urlpatterns = [
    path('index/', bodIndex, name="index")
]