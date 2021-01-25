from django.urls import path

from cssf.views.tl.views_tl import *

app_name = "tl"

urlpatterns = [
    path('index/', labIndex, name="index"),
    path('registrar/entrega/', entregasustanciatl, name="entregasustancias"),
    path('registrar/informes/', informestl, name="informes"),
    path('inventario/movimiento/', movimientotl, name="movimientoinv"),
    path('inventario/stock/', stocktl, name="stockinv")
]