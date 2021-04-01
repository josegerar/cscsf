"""app URL Configuration

The `urlpatterns` list routes URLs to viewsUS. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function viewsUS
    1. Add an import:  from my_app import viewsUS
    2. Add a URL to urlpatterns:  path('', viewsUS.home, name='home')
Class-based viewsUS
    1. Add an import:  from other_app.viewsUS import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urlsUS import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urlsUS'))
"""
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from core.base.views import DashBoard

urlpatterns = [
    path('admin/', admin.site.urls, name="admin"),
    path('', include("core.representantetecnico.urls")),
    path('', include("core.tecnicolaboratorio.urls")),
    path('', include("core.bodega.urls")),
    path('', include('core.login.urls')),
    path('dashboard/', DashBoard.as_view(), name="dashboard"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
