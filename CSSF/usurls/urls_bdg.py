from django.urls import path

from CSSF.usviews.views_bdg import bodIndex

urlpatterns = [
    path('index/', bodIndex, name="indexBod")
]