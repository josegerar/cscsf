from django.urls import path

from cssf.views.bdg.views_bdg import *

app_name = "bdg"

urlpatterns = [
    path('index/', bodIndex, name="index"),
    path('registrar/compras/', ingresarcomprabdg, name="ingresocompras"),
    path('registrar/entrega/', entregasustanciabdg, name="entragasustancias"),
    path('inventario/movimiento/', movimientobdg, name="movimientoinv"),
    path('inventario/stock/', stockbdg, name="stockinv")
]