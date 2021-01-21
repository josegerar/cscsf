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

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cssf/', include('CSSF.urls'))
]
