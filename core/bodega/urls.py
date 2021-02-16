from django.urls import path

from core.bodega.views.views_bdg import bodIndex, ingresarcomprabdg, entregasustanciabdg, movimientobdg, stockbdg

app_name = "bdg"

urlpatterns = [
    path('registrar/compras/', ingresarcomprabdg, name="ingresocompras"),
    path('registrar/entrega/', entregasustanciabdg, name="entragasustancias"),
    path('movimientosinventario/movimiento/', movimientobdg, name="movimientoinv"),
    path('movimientosinventario/stock/', stockbdg, name="stockinv")
]