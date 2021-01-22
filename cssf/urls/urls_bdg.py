from django.urls import path

from cssf.views.bdg.views_bdg import bodIndex

app_name = "bdg"

urlpatterns = [
    path('index/', bodIndex, name="index")
]