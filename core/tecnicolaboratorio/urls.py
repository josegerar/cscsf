from django.urls import path

from core.tecnicolaboratorio.views.views_tl import labIndex, entregasustanciatl, informestl, movimientotl, stocktl

app_name = "tl"

urlpatterns = [
    path('registrar/entrega/', entregasustanciatl, name="entregasustancias"),
    path('registrar/informes/', informestl, name="informes"),
    path('movimientosinventario/movimiento/', movimientotl, name="movimientoinv"),
    path('movimientosinventario/stock/', stocktl, name="stockinv")
]